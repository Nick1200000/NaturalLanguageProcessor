# NLP Analyzer User Guide

## Table of Contents
- [Introduction](#introduction)
- [Getting Started](#getting-started)
- [Features](#features)
- [Subscription Tiers](#subscription-tiers)
- [Using the Analyzer](#using-the-analyzer)
- [Dashboard](#dashboard)
- [Saving and Managing Analyses](#saving-and-managing-analyses)
- [API Access](#api-access)
- [Troubleshooting](#troubleshooting)
- [Contact Support](#contact-support)

## Introduction

NLP Analyzer is a powerful text analysis tool that helps you extract insights from your text data using Natural Language Processing (NLP) techniques. Whether you're analyzing customer feedback, research papers, or social media content, NLP Analyzer provides you with valuable text metrics and visualizations.

## Getting Started

### Creating an Account

1. Visit the NLP Analyzer homepage at [https://nlp-analyzer.example.com](https://nlp-analyzer.example.com)
2. Click the "Sign Up" button in the top right corner
3. Fill in your details (username, email, password)
4. Click "Register" to create your account
5. You'll be automatically logged in and directed to your dashboard

### Logging In

1. Visit the NLP Analyzer homepage
2. Click the "Login" button in the top right corner
3. Enter your email and password
4. Click "Login" to access your account

## Features

NLP Analyzer offers a comprehensive suite of text analysis tools:

- **Sentiment Analysis**: Determine the emotional tone of your text (positive, negative, or neutral)
- **Text Summarization**: Generate concise summaries of lengthy documents
- **Named Entity Recognition**: Identify organizations, people, locations, and other entities
- **Keyword Extraction**: Discover the most important keywords in your text
- **Word Frequency Analysis**: Visualize the most common words with interactive charts

## Subscription Tiers

NLP Analyzer offers different subscription tiers to meet your needs:

### Free Tier
- Up to 5 analyses per day
- Maximum text length: 3,000 characters
- Basic NLP features
- Export formats: TXT

### Standard Tier
- Up to 25 analyses per day
- Maximum text length: 10,000 characters
- All basic NLP features
- Export formats: TXT, CSV, JSON

### Premium Tier
- Up to 100 analyses per day
- Maximum text length: 50,000 characters
- Advanced NLP features
- API access for integration
- Export formats: TXT, CSV, JSON, PDF, DOCX
- Priority support

## Using the Analyzer

### Basic Text Analysis

1. From your dashboard, click "New Analysis" or go to the home page
2. Enter or paste your text in the input area
3. Click "Analyze Text" to process your content
4. View the results in the interactive dashboard below
5. (Optional) Click "Save Analysis" to store it in your account

### Sample Texts

If you want to see how the analyzer works, you can click "Load Sample Text" to populate the text area with a pre-written example.

## Dashboard

Your dashboard is the central hub for managing your NLP Analyzer account:

- **Recent Analyses**: Quick access to your recent text analyses
- **Usage Statistics**: Track your daily and monthly usage
- **Subscription Details**: View your current plan and limits
- **Account Settings**: Update your profile and password

## Saving and Managing Analyses

### Saving an Analysis

After analyzing text, you can save it to your account:

1. Enter a title for your analysis
2. Click "Save Analysis"
3. The analysis will be stored in your account for future reference

### Viewing Saved Analyses

1. Navigate to your dashboard
2. Find the analysis in your "Recent Analyses" list
3. Click on the analysis title to view the full results

### Deleting Analyses

1. From your dashboard or the analysis view page
2. Click the "Delete" button next to the analysis
3. Confirm the deletion when prompted

## API Access

Premium subscribers can access our API for programmatic text analysis:

### Authentication

All API requests require an API key which can be found in your account settings.

```
X-API-Key: your_api_key_here
```

### Endpoints

**POST /api/v1/analyze**

Analyze text and return NLP results.

Request body:
```json
{
  "text": "Your text to analyze",
  "operations": ["sentiment", "entities", "summary", "keywords"]
}
```

Response:
```json
{
  "sentiment": {
    "compound": 0.7256,
    "positive": 0.8,
    "negative": 0.1,
    "neutral": 0.1,
    "sentiment": "positive"
  },
  "entities": {
    "PERSON": ["John Smith"],
    "ORG": ["Google", "Microsoft"],
    "LOC": ["New York"]
  },
  "summary": "Summarized text appears here.",
  "keywords": ["important", "keywords", "extracted"]
}
```

For full API documentation, visit the API Docs section in your Premium account.

## Troubleshooting

### Common Issues

- **Can't log in**: Make sure your email and password are correct. You can reset your password if needed.
- **Analysis fails**: Check that your text doesn't exceed your plan's character limit.
- **API access denied**: Verify that your subscription is active and you're using the correct API key.

## Contact Support

If you need assistance, please contact our support team:

- Email: support@nlp-analyzer.example.com
- Support Hours: Monday-Friday, 9am-5pm EST