import re
import nltk
import string
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.chunk import ne_chunk
from nltk.tag import pos_tag
from collections import Counter

# Download required NLTK resources
# Force download all required resources to ensure they're available
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('vader_lexicon')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('wordnet')
nltk.download('punkt_tab', quiet=True, raise_on_error=False)
nltk.download('averaged_perceptron_tagger_eng', quiet=True, raise_on_error=False)
nltk.download('maxent_ne_chunker_tab', quiet=True, raise_on_error=False)

# Initialize NLTK components
sia = SentimentIntensityAnalyzer()
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('english'))

def preprocess_text(text):
    """Clean and preprocess text for NLP analysis."""
    try:
        # Convert to lowercase
        text = text.lower()
        
        # Remove URLs
        text = re.sub(r'https?://\S+|www\.\S+', '', text)
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in stop_words]
        
        return tokens, text
    except Exception as e:
        print(f"Error in text preprocessing: {str(e)}")
        # Return minimal processed tokens if an error occurs
        return [], text

def analyze_sentiment(text):
    """Analyze sentiment of the given text."""
    if not text:
        return {"error": "No text provided"}
    
    try:
        scores = sia.polarity_scores(text)
        
        # Determine sentiment category
        compound = scores['compound']
        if compound >= 0.05:
            sentiment = "positive"
        elif compound <= -0.05:
            sentiment = "negative"
        else:
            sentiment = "neutral"
        
        return {
            "compound": round(scores['compound'], 2),
            "positive": round(scores['pos'], 2),
            "negative": round(scores['neg'], 2),
            "neutral": round(scores['neu'], 2),
            "sentiment": sentiment
        }
    except Exception as e:
        print(f"Error in sentiment analysis: {str(e)}")
        # Return neutral sentiment if analysis fails
        return {
            "compound": 0,
            "positive": 0,
            "negative": 0,
            "neutral": 1,
            "sentiment": "neutral"
        }

def extract_entities(text):
    """Extract named entities from the text."""
    if not text:
        return {"error": "No text provided"}
    
    try:
        # Tokenize, POS tag, and extract named entities
        tokens = word_tokenize(text)
        pos_tags = pos_tag(tokens)
        named_entities = ne_chunk(pos_tags)
        
        # Process the named entities tree
        entities = {
            "PERSON": [],
            "ORGANIZATION": [],
            "LOCATION": [],
            "DATE": [],
            "TIME": [],
            "MONEY": [],
            "PERCENT": [],
            "FACILITY": [],
            "GPE": []  # Geo-Political Entity
        }
        
        # Extract entities from the tree
        for chunk in named_entities:
            if hasattr(chunk, 'label'):
                entity_type = chunk.label()
                entity_text = ' '.join(c[0] for c in chunk)
                
                if entity_type in entities:
                    if entity_text not in entities[entity_type]:
                        entities[entity_type].append(entity_text)
        
        # Clean up empty categories
        return {k: v for k, v in entities.items() if v}
    except Exception as e:
        print(f"Error in entity extraction: {str(e)}")
        # Return empty result if there's an error
        return {}

def summarize_text(text, ratio=0.3):
    """Generate a simple extractive summary of the text."""
    if not text or len(text) < 50:
        return text
    
    try:
        # Split into sentences
        sentences = sent_tokenize(text)
        
        if len(sentences) <= 2:
            return text
        
        # Preprocess sentences
        clean_sentences = []
        for sentence in sentences:
            clean_sentence = sentence.lower()
            clean_sentence = re.sub(r'[^\w\s]', '', clean_sentence)
            clean_sentences.append(clean_sentence)
        
        # Calculate sentence scores based on word frequency
        word_frequencies = Counter()
        for sentence in clean_sentences:
            for word in word_tokenize(sentence):
                if word not in stop_words:
                    word_frequencies[word] += 1
        
        # Normalize frequencies
        max_frequency = max(word_frequencies.values()) if word_frequencies else 1
        for word in word_frequencies:
            word_frequencies[word] = int(word_frequencies[word] / max_frequency * 100) / 100  # Convert to int for compatibility
        
        # Score sentences
        sentence_scores = {}
        for i, sentence in enumerate(clean_sentences):
            for word in word_tokenize(sentence):
                if word in word_frequencies:
                    if i not in sentence_scores:
                        sentence_scores[i] = 0
                    sentence_scores[i] += word_frequencies[word]
        
        # Get top sentences
        num_sentences = max(1, int(len(sentences) * ratio))
        top_sentences = sorted(sentence_scores.items(), key=lambda x: x[1], reverse=True)[:num_sentences]
        top_sentences = sorted(top_sentences, key=lambda x: x[0])
        
        # Create summary
        summary = [sentences[i] for i, _ in top_sentences]
        
        return ' '.join(summary)
    except Exception as e:
        print(f"Error in text summarization: {str(e)}")
        # Return original text if summarization fails
        return text

def extract_keywords(text, num_keywords=10):
    """Extract the most important keywords from the text."""
    if not text:
        return []
    
    try:
        tokens, _ = preprocess_text(text)
        
        # Count word frequencies
        word_freq = Counter(tokens)
        
        # Get most common words (keywords)
        keywords = [word for word, count in word_freq.most_common(num_keywords)]
        
        return keywords
    except Exception as e:
        print(f"Error in keyword extraction: {str(e)}")
        return []  # Return empty list if there's an error

def get_word_frequencies(text, top_n=20):
    """Get word frequencies for visualization."""
    if not text:
        return []
    
    try:
        tokens, _ = preprocess_text(text)
        
        # Count word frequencies
        word_freq = Counter(tokens)
        
        # Get top N words
        top_words = word_freq.most_common(top_n)
        
        # Format for visualization
        result = [{"word": word, "frequency": count} for word, count in top_words]
        
        return result
    except Exception as e:
        print(f"Error in word frequency analysis: {str(e)}")
        return []  # Return empty list if there's an error
