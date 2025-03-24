import os
import logging
import secrets
import datetime
from functools import wraps
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from models import db, User, Analysis, ApiUsage
from nlp_processor import (
    analyze_sentiment, 
    extract_entities, 
    summarize_text,
    extract_keywords,
    get_word_frequencies
)

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Create the Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", 'sqlite:///nlp_analyzer.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = os.environ.get("SESSION_SECRET", secrets.token_hex(16))

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create database tables if they don't exist
with app.app_context():
    db.create_all()

# Custom decorators
def check_subscription_limits(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            # Get user limits
            limits = current_user.get_tier_limits()
            
            # Check daily analysis limit
            today = datetime.datetime.utcnow().date()
            today_start = datetime.datetime.combine(today, datetime.time.min)
            today_end = datetime.datetime.combine(today, datetime.time.max)
            
            analyses_today = Analysis.query.filter(
                Analysis.user_id == current_user.id,
                Analysis.created_at.between(today_start, today_end)
            ).count()
            
            if analyses_today >= limits['analyses_per_day']:
                flash('You have reached your daily analysis limit. Please upgrade your subscription for more analyses.', 'warning')
                return redirect(url_for('dashboard'))
                
        return f(*args, **kwargs)
    return decorated_function

# Route definitions
@app.route('/')
def index():
    """Render the main page of the application."""
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page"""
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash('Login successful!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('dashboard'))
        else:
            flash('Invalid email or password', 'danger')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page"""
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Check if user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists. Please try another.', 'danger')
            return render_template('register.html')
            
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
        
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    """Log the user out"""
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('index'))

@app.route('/dashboard')
@login_required
def dashboard():
    """User dashboard showing saved analyses and subscription info"""
    recent_analyses = Analysis.query.filter_by(user_id=current_user.id).order_by(Analysis.created_at.desc()).limit(5).all()
    limits = current_user.get_tier_limits()
    
    # Get daily usage
    today = datetime.datetime.utcnow().date()
    today_start = datetime.datetime.combine(today, datetime.time.min)
    today_end = datetime.datetime.combine(today, datetime.time.max)
    
    analyses_today = Analysis.query.filter(
        Analysis.user_id == current_user.id,
        Analysis.created_at.between(today_start, today_end)
    ).count()
    
    return render_template(
        'dashboard.html',
        user=current_user,
        analyses=recent_analyses,
        limits=limits,
        usage={
            'analyses_today': analyses_today,
            'limit': limits['analyses_per_day']
        }
    )

@app.route('/analyze', methods=['POST'])
def analyze():
    """Process the text and return NLP analysis results."""
    try:
        text = request.form.get('text', '')
        
        if not text:
            return jsonify({
                'error': 'No text provided for analysis'
            }), 400
        
        # For demo purposes, let's remove the character limit
        # Only keep a very high limit to prevent abuse
        if current_user.is_authenticated:
            limits = current_user.get_tier_limits()
            if len(text) > 100000:  # Very high limit to prevent abuse
                return jsonify({
                    'error': f'Text exceeds 100,000 character limit. Please shorten your text.'
                }), 403
        elif len(text) > 100000:  # Same high limit for guest users
            return jsonify({
                'error': 'Text exceeds 100,000 character limit. Please shorten your text.'
            }), 403
            
        # Perform NLP analyses
        sentiment_result = analyze_sentiment(text)
        entities_result = extract_entities(text)
        summary_result = summarize_text(text)
        keywords_result = extract_keywords(text)
        word_freq = get_word_frequencies(text)
        
        # Save analysis if user is logged in
        if current_user.is_authenticated:
            analysis = Analysis(
                user_id=current_user.id,
                content=text,
                summary=summary_result,
                sentiment=sentiment_result.get('compound', 0)
            )
            
            results = {
                'sentiment': sentiment_result,
                'entities': entities_result,
                'keywords': keywords_result,
                'wordFrequencies': word_freq
            }
            analysis.set_results(results)
            
            db.session.add(analysis)
            db.session.commit()
        
        return jsonify({
            'sentiment': sentiment_result,
            'entities': entities_result,
            'summary': summary_result,
            'keywords': keywords_result,
            'wordFrequencies': word_freq
        })
        
    except Exception as e:
        logger.error(f"Error during analysis: {str(e)}")
        return jsonify({
            'error': f'Analysis failed: {str(e)}'
        }), 500

@app.route('/analyze/save', methods=['POST'])
@login_required
@check_subscription_limits
def save_analysis():
    """Save an analysis with a title"""
    try:
        title = request.form.get('title', 'Untitled Analysis')
        text = request.form.get('text', '')
        
        if not text:
            flash('No text provided for analysis', 'danger')
            return redirect(url_for('dashboard'))
            
        # Perform NLP analyses
        sentiment_result = analyze_sentiment(text)
        entities_result = extract_entities(text)
        summary_result = summarize_text(text)
        keywords_result = extract_keywords(text)
        word_freq = get_word_frequencies(text)
        
        # Save the analysis
        analysis = Analysis(
            user_id=current_user.id,
            title=title,
            content=text,
            summary=summary_result,
            sentiment=sentiment_result.get('compound', 0)
        )
        
        results = {
            'sentiment': sentiment_result,
            'entities': entities_result,
            'keywords': keywords_result,
            'wordFrequencies': word_freq
        }
        analysis.set_results(results)
        
        db.session.add(analysis)
        db.session.commit()
        
        flash('Analysis saved successfully!', 'success')
        return redirect(url_for('view_analysis', analysis_id=analysis.id))
        
    except Exception as e:
        logger.error(f"Error saving analysis: {str(e)}")
        flash(f'Error saving analysis: {str(e)}', 'danger')
        return redirect(url_for('dashboard'))

@app.route('/analysis/<int:analysis_id>')
@login_required
def view_analysis(analysis_id):
    """View a saved analysis"""
    analysis = Analysis.query.get_or_404(analysis_id)
    
    # Check if the analysis belongs to the current user
    if analysis.user_id != current_user.id:
        flash('You do not have permission to view this analysis', 'danger')
        return redirect(url_for('dashboard'))
    
    results = analysis.get_results()
    
    return render_template(
        'view_analysis.html',
        analysis=analysis,
        results=results
    )

@app.route('/analysis/<int:analysis_id>/delete', methods=['POST'])
@login_required
def delete_analysis(analysis_id):
    """Delete a saved analysis"""
    analysis = Analysis.query.get_or_404(analysis_id)
    
    # Check if the analysis belongs to the current user
    if analysis.user_id != current_user.id:
        flash('You do not have permission to delete this analysis', 'danger')
        return redirect(url_for('dashboard'))
    
    db.session.delete(analysis)
    db.session.commit()
    
    flash('Analysis deleted successfully', 'success')
    return redirect(url_for('dashboard'))

@app.route('/subscription')
@login_required
def subscription():
    """Subscription management page"""
    return render_template('subscription.html', user=current_user)

@app.route('/api/docs')
@login_required
def api_docs():
    """API documentation page - only for premium users"""
    if not current_user.is_premium():
        flash('API access is only available for Premium subscribers', 'warning')
        return redirect(url_for('subscription'))
    
    return render_template('api_docs.html', user=current_user)

# API Endpoints
@app.route('/api/v1/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for text analysis"""
    # Check for API key authentication
    api_key = request.headers.get('X-API-Key')
    if not api_key:
        return jsonify({'error': 'API key is required'}), 401
    
    user = User.query.filter_by(api_key=api_key).first()
    if not user or not user.is_premium():
        return jsonify({'error': 'Invalid API key or insufficient subscription tier'}), 403
    
    # Process the request
    start_time = datetime.datetime.now()
    
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Text field is required'}), 400
        
        text = data['text']
        
        # Check text length
        limits = user.get_tier_limits()
        if len(text) > limits['text_length']:
            return jsonify({
                'error': f'Text exceeds the {limits["text_length"]} character limit for your subscription tier.'
            }), 403
        
        # Perform analyses based on requested operations
        operations = data.get('operations', ['sentiment', 'entities', 'summary', 'keywords'])
        result = {}
        
        if 'sentiment' in operations:
            result['sentiment'] = analyze_sentiment(text)
        
        if 'entities' in operations:
            result['entities'] = extract_entities(text)
        
        if 'summary' in operations:
            result['summary'] = summarize_text(text)
        
        if 'keywords' in operations:
            result['keywords'] = extract_keywords(text)
        
        if 'word_frequencies' in operations:
            result['wordFrequencies'] = get_word_frequencies(text)
        
        # Log API usage
        response_time = (datetime.datetime.now() - start_time).total_seconds()
        api_usage = ApiUsage(
            user_id=user.id,
            endpoint='/api/v1/analyze',
            status_code=200,
            response_time=response_time
        )
        db.session.add(api_usage)
        db.session.commit()
        
        return jsonify(result)
        
    except Exception as e:
        # Log error and API usage
        response_time = (datetime.datetime.now() - start_time).total_seconds()
        api_usage = ApiUsage(
            user_id=user.id,
            endpoint='/api/v1/analyze',
            status_code=500,
            response_time=response_time
        )
        db.session.add(api_usage)
        db.session.commit()
        
        logger.error(f"API error during analysis: {str(e)}")
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
