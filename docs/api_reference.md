# NLP Analyzer API Reference

## Overview

The NLP Analyzer API allows Premium tier subscribers to access NLP analysis features programmatically. This document provides a comprehensive reference for all available endpoints, parameters, and response formats.

## Base URL

```
https://api.nlp-analyzer.example.com/v1
```

## Authentication

All API requests require authentication using an API key. You can find your API key in your account settings page when logged in with a Premium subscription.

Include your API key in the request header:

```
X-API-Key: your_api_key_here
```

## Rate Limits

The API is subject to rate limiting based on your subscription tier:

| Tier | Rate Limit |
|------|------------|
| Premium | 100 requests per day |

Exceeding these limits will result in a `429 Too Many Requests` response.

## Endpoints

### Text Analysis

#### POST /analyze

Performs NLP analysis on the provided text.

**Request**

```http
POST /analyze
Content-Type: application/json
X-API-Key: your_api_key_here

{
  "text": "Your text to analyze",
  "operations": ["sentiment", "entities", "summary", "keywords", "word_frequency"],
  "options": {
    "summary_ratio": 0.3,
    "max_keywords": 10,
    "min_keyword_frequency": 2
  }
}
```

**Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| text | string | Yes | The text content to analyze |
| operations | array | No | Array of operations to perform. Default is all operations. |
| options | object | No | Additional options for specific operations |

Available operations:
- `sentiment`: Sentiment analysis
- `entities`: Named entity recognition
- `summary`: Text summarization
- `keywords`: Keyword extraction
- `word_frequency`: Word frequency analysis

Options:
- `summary_ratio`: Percentage of text to include in summary (0.1-0.5, default: 0.3)
- `max_keywords`: Maximum number of keywords to return (5-30, default: 10)
- `min_keyword_frequency`: Minimum frequency for keywords (1-10, default: 2)

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "request_id": "req_12345",
  "timestamp": "2025-03-24T12:34:56Z",
  "text_length": 243,
  "results": {
    "sentiment": {
      "compound": 0.8402,
      "positive": 0.7,
      "negative": 0.05,
      "neutral": 0.25,
      "sentiment": "positive"
    },
    "entities": {
      "PERSON": ["John Smith", "Jane Doe"],
      "ORG": ["Google", "Microsoft"],
      "LOC": ["New York", "San Francisco"],
      "DATE": ["January 15th", "next week"]
    },
    "summary": "This is a summarized version of the original text.",
    "keywords": [
      {"word": "important", "score": 0.89},
      {"word": "analysis", "score": 0.75},
      {"word": "keywords", "score": 0.68}
    ],
    "word_frequency": [
      {"word": "text", "count": 12},
      {"word": "analysis", "count": 8},
      {"word": "data", "count": 6}
    ]
  }
}
```

**Error Responses**

```http
HTTP/1.1 400 Bad Request
Content-Type: application/json

{
  "error": "invalid_request",
  "message": "Text exceeds maximum allowed length",
  "request_id": "req_12345"
}
```

```http
HTTP/1.1 401 Unauthorized
Content-Type: application/json

{
  "error": "unauthorized",
  "message": "Invalid API key",
  "request_id": "req_12345"
}
```

```http
HTTP/1.1 429 Too Many Requests
Content-Type: application/json

{
  "error": "rate_limit_exceeded",
  "message": "You have exceeded your daily rate limit",
  "request_id": "req_12345"
}
```

### Account Information

#### GET /account

Retrieves information about the current API user account.

**Request**

```http
GET /account
X-API-Key: your_api_key_here
```

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "account": {
    "username": "user123",
    "subscription_tier": "premium",
    "subscription_expires": "2025-12-31T23:59:59Z",
    "daily_limit": 100,
    "daily_usage": 45,
    "remaining_requests": 55
  }
}
```

### Usage Statistics

#### GET /usage

Retrieves API usage statistics for the authenticated user.

**Request**

```http
GET /usage
X-API-Key: your_api_key_here
```

**Parameters**

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| start_date | string | No | Start date for usage stats (YYYY-MM-DD) |
| end_date | string | No | End date for usage stats (YYYY-MM-DD) |

**Response**

```http
HTTP/1.1 200 OK
Content-Type: application/json

{
  "usage": {
    "total_requests": 1250,
    "period": {
      "start": "2025-01-01",
      "end": "2025-03-24"
    },
    "daily_usage": [
      {"date": "2025-03-24", "requests": 45},
      {"date": "2025-03-23", "requests": 38},
      {"date": "2025-03-22", "requests": 52}
    ],
    "operations": {
      "sentiment": 1134,
      "entities": 982,
      "summary": 1056,
      "keywords": 1150,
      "word_frequency": 876
    }
  }
}
```

## Status Codes

| Code | Description |
|------|-------------|
| 200 | Successful operation |
| 400 | Bad request - invalid parameters |
| 401 | Unauthorized - invalid or missing API key |
| 403 | Forbidden - insufficient permissions |
| 404 | Not found - endpoint doesn't exist |
| 429 | Too many requests - rate limit exceeded |
| 500 | Server error |

## Error Handling

All error responses have the following format:

```json
{
  "error": "error_code",
  "message": "Human-readable error message",
  "request_id": "unique_request_identifier"
}
```

Common error codes:

| Error Code | Description |
|------------|-------------|
| invalid_request | The request is invalid or missing required parameters |
| invalid_api_key | The provided API key is invalid |
| subscription_required | A Premium subscription is required for this operation |
| rate_limit_exceeded | You have exceeded your rate limit |
| text_too_long | The provided text exceeds the maximum allowed length |
| server_error | An internal server error occurred |

## Examples

### Python Example

```python
import requests
import json

API_KEY = "your_api_key"
API_URL = "https://api.nlp-analyzer.example.com/v1"

headers = {
    "Content-Type": "application/json",
    "X-API-Key": API_KEY
}

payload = {
    "text": "Natural language processing (NLP) is a subfield of linguistics, computer science, and artificial intelligence concerned with the interactions between computers and human language.",
    "operations": ["sentiment", "keywords"]
}

response = requests.post(f"{API_URL}/analyze", headers=headers, json=payload)

if response.status_code == 200:
    results = response.json()
    print(json.dumps(results, indent=2))
else:
    print(f"Error: {response.status_code}")
    print(response.json())
```

### JavaScript Example

```javascript
const apiKey = 'your_api_key';
const apiUrl = 'https://api.nlp-analyzer.example.com/v1';

const analyzeText = async (text) => {
  try {
    const response = await fetch(`${apiUrl}/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'X-API-Key': apiKey
      },
      body: JSON.stringify({
        text: text,
        operations: ['sentiment', 'entities', 'summary']
      })
    });
    
    if (!response.ok) {
      const errorData = await response.json();
      throw new Error(`API Error: ${errorData.message}`);
    }
    
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error analyzing text:', error);
    throw error;
  }
};

// Usage
analyzeText('Your text to analyze')
  .then(results => {
    console.log('Analysis results:', results);
  })
  .catch(error => {
    console.error('Failed to analyze text:', error);
  });
```

## Further Resources

- [API Change Log](/api/changelog)
- [Common Use Cases](/api/use-cases)
- [API SDKs and Libraries](/api/libraries)