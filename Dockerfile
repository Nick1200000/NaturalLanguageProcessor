FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY pyproject.toml uv.lock /app/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -e .

# Download NLTK data
RUN python -m nltk.downloader punkt stopwords vader_lexicon averaged_perceptron_tagger maxent_ne_chunker words wordnet

# Copy application code
COPY . /app/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000

# Expose the port
EXPOSE 5000

# Run the application
CMD gunicorn --bind 0.0.0.0:$PORT --workers 2 --threads 4 --timeout 120 main:app