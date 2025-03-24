from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
import json

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    subscription_tier = db.Column(db.String(20), default="free")  # free, standard, premium
    subscription_expires = db.Column(db.DateTime, nullable=True)
    api_key = db.Column(db.String(64), unique=True, nullable=True)
    
    # Relationship with Analysis
    analyses = db.relationship('Analysis', backref='user', lazy='dynamic', cascade="all, delete-orphan")
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def is_premium(self):
        """Check if user has premium subscription"""
        return (self.subscription_tier == "premium" and 
                (self.subscription_expires is None or 
                 self.subscription_expires > datetime.datetime.utcnow()))
                 
    def is_standard(self):
        """Check if user has standard subscription"""
        return (self.subscription_tier == "standard" and 
                (self.subscription_expires is None or 
                 self.subscription_expires > datetime.datetime.utcnow()))
                 
    def get_tier_limits(self):
        """Get limits based on subscription tier"""
        if self.is_premium():
            return {
                "text_length": 50000,  # characters
                "analyses_per_day": 100,
                "export_formats": ["pdf", "csv", "json", "docx"],
                "advanced_nlp": True,
                "batch_processing": True,
                "api_access": True
            }
        elif self.is_standard():
            return {
                "text_length": 10000,  # characters
                "analyses_per_day": 30,
                "export_formats": ["pdf", "csv"],
                "advanced_nlp": True,
                "batch_processing": False,
                "api_access": False
            }
        else:  # Free tier
            return {
                "text_length": 3000,  # characters
                "analyses_per_day": 5,
                "export_formats": ["csv"],
                "advanced_nlp": False,
                "batch_processing": False,
                "api_access": False
            }


class Analysis(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(120), nullable=True)
    content = db.Column(db.Text, nullable=False)
    summary = db.Column(db.Text, nullable=True)
    sentiment = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    
    # Store analysis results as JSON
    results_json = db.Column(db.Text, nullable=True)
    
    def set_results(self, results_dict):
        """Store analysis results as JSON"""
        self.results_json = json.dumps(results_dict)
    
    def get_results(self):
        """Get analysis results from JSON"""
        if self.results_json:
            return json.loads(self.results_json)
        return None


class ApiUsage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    endpoint = db.Column(db.String(120), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    status_code = db.Column(db.Integer, nullable=False)
    response_time = db.Column(db.Float, nullable=True)  # in seconds
    
    # Relationship
    user = db.relationship('User', backref=db.backref('api_usage', lazy='dynamic'))