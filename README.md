# NLP Text Analyzer

## Overview
NLP Text Analyzer is a web application that demonstrates various natural language processing techniques to analyze text. It features sentiment analysis, entity recognition, text summarization, keyword extraction, and interactive visualizations.

The application is designed to be responsive and user-friendly, providing immediate insights into the text that you input. It's a great example of how NLP can be used to extract meaningful information from unstructured text data.

## Features

- **Text Summarization**: Extract the key points from long texts
- **Sentiment Analysis**: Determine if the text conveys positive, negative, or neutral sentiment
- **Named Entity Recognition**: Identify and categorize named entities (people, organizations, locations, etc.)
- **Keyword Extraction**: Identify the most important terms in the text
- **Word Frequency Analysis**: Visualize the most commonly used words
- **Interactive Visualizations**: See the results through charts and visual elements
- **Responsive Design**: Works on desktop, tablet, and mobile devices

## Technologies Used

- **Backend**: Flask (Python web framework)
- **NLP Processing**: NLTK (Natural Language Toolkit)
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Bootstrap 5
- **Visualizations**: Chart.js

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Pip (Python package installer)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/nlp-text-analyzer.git
   cd nlp-text-analyzer
   ```

2. Install the required packages:
   ```
   pip install flask nltk
   ```

3. Download NLTK data (will be downloaded automatically on first run, but you can do it manually):
   ```python
   import nltk
   nltk.download('punkt')
   nltk.download('stopwords')
   nltk.download('vader_lexicon')
   nltk.download('averaged_perceptron_tagger')
   nltk.download('maxent_ne_chunker')
   nltk.download('words')
   nltk.download('wordnet')
   ```

### Running the Application

1. Start the Flask server:
   ```
   python main.py
   ```

2. Open your web browser and go to `http://localhost:5000`

## Usage

1. Enter or paste text into the text area (or use the "Try Sample Text" button)
2. Click "Analyze Text" or press Ctrl+Enter
3. View the analysis results in the various sections:
   - Summary
   - Sentiment Analysis
   - Word Frequency
   - Named Entities
   - Keywords

## Project Structure

