# NLP Text Analyzer

![NLP Text Analyzer Banner](https://i.imgur.com/RqNW1WT.png)

## Overview
NLP Text Analyzer is a web application that demonstrates various natural language processing techniques to analyze text. It features sentiment analysis, entity recognition, text summarization, keyword extraction, and interactive visualizations.

The application is designed to be responsive and user-friendly, providing immediate insights into the text that you input. It's a great example of how NLP can be used to extract meaningful information from unstructured text data.

## Demo
![Application Demo](https://i.imgur.com/bHQd82R.gif)

## Features

- **Text Summarization**: Extract the key points from long texts
- **Sentiment Analysis**: Determine if the text conveys positive, negative, or neutral sentiment
- **Named Entity Recognition**: Identify and categorize named entities (people, organizations, locations, etc.)
- **Keyword Extraction**: Identify the most important terms in the text
- **Word Frequency Analysis**: Visualize the most commonly used words
- **Interactive Visualizations**: See the results through charts and visual elements
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Error Handling**: Robust error handling for a smooth user experience

## Technologies Used

- **Backend**: Flask (Python web framework)
- **NLP Processing**: NLTK (Natural Language Toolkit)
- **Frontend**: HTML, CSS, JavaScript
- **Styling**: Bootstrap 5 (Dark Theme)
- **Visualizations**: Chart.js
- **Icons**: Font Awesome

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
   pip install flask nltk gunicorn flask-sqlalchemy email-validator psycopg2-binary
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

2. For production deployment:
   ```
   gunicorn --bind 0.0.0.0:5000 main:app
   ```

3. Open your web browser and go to `http://localhost:5000`

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

```
├── static/                  # Static assets
│   ├── css/                 # CSS styles
│   │   └── custom.css       # Custom styling beyond Bootstrap
│   └── js/                  # JavaScript files
│       └── app.js           # Main application logic
├── templates/               # HTML templates
│   ├── index.html           # Main page template
│   └── layout.html          # Base layout template
├── app.py                   # Flask application routes and configuration
├── main.py                  # Application entry point
├── nlp_processor.py         # NLP processing functions
└── README.md                # Project documentation
```

## Key Components

### `app.py`
Contains the Flask application setup, routes, and request handling.

### `nlp_processor.py`
Implements all NLP functionality:
- Text preprocessing
- Sentiment analysis
- Entity extraction
- Text summarization
- Keyword extraction
- Word frequency analysis

### `static/js/app.js`
Handles:
- AJAX requests to the backend
- Chart creation and updates
- Dynamic content rendering
- User interactions

### `templates/`
Contains Jinja2 templates for rendering HTML pages.

## Future Enhancements

- Topic modeling to identify key themes
- Text classification capabilities
- Multilingual support
- User accounts to save analysis history
- Export functionality for reports
- Enhanced visualizations

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- NLTK team for their excellent NLP library
- Bootstrap team for the responsive design framework
- Chart.js contributors for the visualization library

