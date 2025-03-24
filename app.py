import os
import logging
from flask import Flask, render_template, request, jsonify
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
app.secret_key = os.environ.get("SESSION_SECRET")

@app.route('/')
def index():
    """Render the main page of the application."""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Process the text and return NLP analysis results."""
    try:
        text = request.form.get('text', '')
        
        if not text:
            return jsonify({
                'error': 'No text provided for analysis'
            }), 400
            
        # Perform NLP analyses
        sentiment_result = analyze_sentiment(text)
        entities_result = extract_entities(text)
        summary_result = summarize_text(text)
        keywords_result = extract_keywords(text)
        word_freq = get_word_frequencies(text)
        
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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
