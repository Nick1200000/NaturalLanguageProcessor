# NLP Analyzer - Technical Guide

## Table of Contents
- [Installation](#installation)
  - [Prerequisites](#prerequisites)
  - [Local Development Setup](#local-development-setup)
  - [Environment Variables](#environment-variables)
  - [Database Setup](#database-setup)
- [Deployment Options](#deployment-options)
  - [Docker Deployment](#docker-deployment)
  - [Kubernetes Deployment](#kubernetes-deployment)
  - [Traditional Deployment](#traditional-deployment)
- [Architecture](#architecture)
  - [Application Structure](#application-structure)
  - [Database Schema](#database-schema)
  - [Key Components](#key-components)
- [Development](#development)
  - [Adding New NLP Features](#adding-new-nlp-features)
  - [Modifying the Frontend](#modifying-the-frontend)
  - [Adding API Endpoints](#adding-api-endpoints)
- [Testing](#testing)
- [CI/CD](#cicd)
- [Contributing](#contributing)
- [License](#license)

## Installation

### Prerequisites

To run NLP Analyzer, you'll need:

- Python 3.9 or higher
- PostgreSQL 13 or higher
- pip (Python package manager)
- NLTK resources

### Local Development Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/nlp-analyzer.git
   cd nlp-analyzer
   ```

2. Install dependencies:
   ```bash
   pip install -e .
   ```

3. Download required NLTK resources:
   ```bash
   python -c "import nltk; nltk.download(['punkt', 'stopwords', 'vader_lexicon', 'averaged_perceptron_tagger', 'maxent_ne_chunker', 'words', 'wordnet'])"
   ```

4. Set up environment variables (see next section)

5. Initialize the database:
   ```bash
   flask db upgrade
   ```

6. Run the development server:
   ```bash
   python main.py
   ```

7. Access the application at http://localhost:5000

### Environment Variables

Create a `.env` file in the project root with the following variables:

```
DATABASE_URL=postgresql://username:password@localhost:5432/nlp_analyzer
SESSION_SECRET=your-secure-session-key
FLASK_ENV=development
```

Required environment variables:

| Variable | Description | Example |
|----------|-------------|---------|
| DATABASE_URL | PostgreSQL connection string | postgresql://user:pass@localhost:5432/dbname |
| SESSION_SECRET | Secret key for Flask sessions | random-secure-string |
| FLASK_ENV | Environment (development/production) | production |

### Database Setup

1. Create a PostgreSQL database:
   ```bash
   createdb nlp_analyzer
   ```

2. The application will automatically create the necessary tables when first run with the correct DATABASE_URL.

## Deployment Options

### Docker Deployment

The application includes a Dockerfile and docker-compose.yml for containerized deployment:

1. Build and run using Docker Compose:
   ```bash
   docker-compose up -d
   ```

2. Access the application at http://localhost:5000

### Kubernetes Deployment

For production environments, we provide Kubernetes manifests in the `k8s/` directory:

1. Create the required secrets:
   ```bash
   kubectl create secret generic nlp-analyzer-secrets \
     --from-literal=DATABASE_URL="postgresql://user:pass@postgres:5432/nlp_analyzer" \
     --from-literal=SESSION_SECRET="your-secure-key"
   ```

2. Apply the Kubernetes manifests:
   ```bash
   kubectl apply -f k8s/
   ```

3. Access the application via the service (LoadBalancer or Ingress)

### Traditional Deployment

For traditional servers:

1. Clone the repository and install dependencies as shown in the Local Development Setup
2. Configure a production WSGI server (gunicorn, uwsgi, etc.)
3. Set up a reverse proxy (nginx, Apache, etc.)

Example systemd service file (`/etc/systemd/system/nlp-analyzer.service`):

```
[Unit]
Description=NLP Analyzer
After=network.target

[Service]
User=appuser
WorkingDirectory=/path/to/nlp-analyzer
ExecStart=/path/to/venv/bin/gunicorn --workers 3 --bind 0.0.0.0:5000 main:app
Restart=on-failure
Environment=DATABASE_URL=postgresql://user:pass@localhost:5432/nlp_analyzer
Environment=SESSION_SECRET=your-secure-session-key
Environment=FLASK_ENV=production

[Install]
WantedBy=multi-user.target
```

## Architecture

### Application Structure

```
nlp-analyzer/
├── app.py            # Main Flask application
├── main.py           # Entry point
├── models.py         # Database models
├── nlp_processor.py  # NLP processing logic
├── static/           # Static files (CSS, JS)
│   ├── css/
│   ├── js/
│   └── img/
├── templates/        # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── dashboard.html
│   └── ...
├── docs/             # Documentation
├── k8s/              # Kubernetes manifests
└── tests/            # Test suite
```

### Database Schema

The application uses SQLAlchemy with the following main models:

- `User`: User accounts and subscription information
- `Analysis`: Saved text analyses with results
- `ApiUsage`: API usage tracking for premium users

Key relationships:
- One-to-many from User to Analysis
- One-to-many from User to ApiUsage

### Key Components

- **Flask Backend**: Handles routes, authentication, and database operations
- **NLP Processor**: Core NLP functionality using NLTK and other libraries
- **Bootstrap Frontend**: Responsive UI with interactive elements
- **Chart.js Visualizations**: Interactive data visualizations
- **User Authentication**: Flask-Login for session management

## Development

### Adding New NLP Features

To add a new NLP processing feature:

1. Add the processing function to `nlp_processor.py`:
   ```python
   def new_nlp_feature(text):
       # Processing logic here
       return result
   ```

2. Update the analyze route in `app.py` to include the new feature:
   ```python
   # Add to analyze function
   results['new_feature'] = nlp_processor.new_nlp_feature(text)
   ```

3. Update the frontend display in the relevant templates and JavaScript

### Modifying the Frontend

The frontend uses Bootstrap for styling and Chart.js for visualizations:

1. Template files are in the `templates/` directory
2. CSS and JavaScript files are in the `static/` directory
3. Main application JavaScript is in `static/js/app.js`

### Adding API Endpoints

To add a new API endpoint:

1. Add the new route to `app.py`:
   ```python
   @app.route('/api/v1/new_endpoint', methods=['POST'])
   @check_subscription_limits
   def api_new_endpoint():
       # API endpoint logic
       return jsonify(results)
   ```

2. Update the API documentation and tests accordingly

## Testing

Run tests using pytest:

```bash
python -m pytest
```

Tests are organized in the `tests/` directory:
- `test_app.py`: Application routes and functionality
- `test_nlp.py`: NLP processing functions
- `test_models.py`: Database models and operations
- `test_api.py`: API endpoints

## CI/CD

The repository includes CI/CD configurations for:

- **GitHub Actions**: `.github/workflows/main.yml`
- **GitLab CI**: `.gitlab-ci.yml`
- **Jenkins**: `Jenkinsfile`

These pipelines:
1. Run tests
2. Build Docker images
3. Deploy to staging/production environments

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/new-feature`
3. Make your changes
4. Run tests: `pytest`
5. Submit a pull request

Please follow the project's code style and include tests for new features.

## License

NLP Analyzer is open-source software licensed under the MIT license. See the LICENSE file for details.