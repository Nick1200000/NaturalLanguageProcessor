# NLP Analyzer

![NLP Analyzer](generated-icon.png)

A powerful text analysis application using Natural Language Processing to extract insights from text data, packaged as both an open-source project and a commercial product.

## Overview

NLP Analyzer is a Flask-based web application that provides sophisticated text analysis features, including:

- Sentiment Analysis
- Named Entity Recognition
- Text Summarization
- Keyword Extraction
- Word Frequency Analysis with Visualizations

The platform is designed for both casual users and professionals who need to extract meaningful insights from text data for research, content analysis, market research, or customer feedback evaluation.

## Features

- **Comprehensive NLP Analysis**: Multiple analysis techniques in one platform
- **Interactive Visualizations**: Chart.js-powered data visualizations
- **Responsive Design**: Mobile-friendly Bootstrap interface
- **User Accounts**: Save and manage your analyses
- **Tiered Subscriptions**: Free, Standard, and Premium tiers with different feature sets
- **API Access**: Programmatic access for Premium users
- **Extensive Documentation**: User guides and API reference

## Installation

### Quick Start with Docker

```bash
# Clone the repository
git clone https://github.com/your-org/nlp-analyzer.git
cd nlp-analyzer

# Start with Docker Compose
docker-compose up -d

# Access at http://localhost:5000
```

### Local Development Setup

```bash
# Clone the repository
git clone https://github.com/your-org/nlp-analyzer.git
cd nlp-analyzer

# Install dependencies
pip install -e .

# Download NLTK resources
python -c "import nltk; nltk.download(['punkt', 'stopwords', 'vader_lexicon', 'averaged_perceptron_tagger', 'maxent_ne_chunker', 'words', 'wordnet'])"

# Set up environment variables
export DATABASE_URL=postgresql://username:password@localhost:5432/nlp_analyzer
export SESSION_SECRET=your-secure-session-key

# Run the application
python main.py
```

## Documentation

- [User Guide](docs/user_guide.md) - End-user documentation
- [Technical Guide](docs/technical_guide.md) - Installation, deployment, and development guide
- [API Reference](docs/api_reference.md) - Complete API documentation for Premium users

## Deployment Options

NLP Analyzer can be deployed in various environments:

- Docker container deployment (Dockerfile included)
- Multi-container setup (docker-compose.yml included)
- Kubernetes cluster (k8s manifests included)
- Traditional server deployment (systemd service example in docs)

CI/CD configurations are included for:
- GitHub Actions
- GitLab CI
- Jenkins

## Screenshots

![Dashboard](static/img/screenshots/dashboard.png)
*User dashboard with saved analyses*

![Analysis Results](static/img/screenshots/analysis.png)
*Interactive analysis results with visualizations*

## License

NLP Analyzer is released under the MIT License. See [LICENSE](LICENSE) for details.

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Support

- For issues and bugs: Submit a GitHub issue
- For feature requests: Submit a GitHub issue with the "enhancement" label
- For commercial support: Contact support@nlp-analyzer.example.com