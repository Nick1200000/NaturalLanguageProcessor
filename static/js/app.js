// DOM elements and event bindings
document.addEventListener('DOMContentLoaded', function() {
    // Initialize elements
    const textInput = document.getElementById('text-input');
    const analyzeButton = document.getElementById('analyze-btn');
    const resultsContainer = document.getElementById('results-container');
    const loadingSpinner = document.getElementById('loading-spinner');
    const errorContainer = document.getElementById('error-container');
    const sampleTextButton = document.getElementById('sample-text-btn');

    // Make elements available globally
    window.textInput = textInput;
    window.resultsContainer = resultsContainer;
    window.loadingSpinner = loadingSpinner;
    window.errorContainer = errorContainer;

    // Charts objects
    window.sentimentChart = null;
    window.wordFreqChart = null;

    // Only add event listeners if elements exist (on pages where the analyzer is present)
    if (analyzeButton && textInput) {
        // Event listener for analyze button
        analyzeButton.addEventListener('click', function() {
            analyzeText();
        });

        // Listen for Enter key in the textarea
        textInput.addEventListener('keydown', function(event) {
            if (event.key === 'Enter' && event.ctrlKey) {
                event.preventDefault();
                analyzeText();
            }
        });
        
        // Set up sample text button
        if (sampleTextButton) {
            sampleTextButton.addEventListener('click', loadSampleText);
        }
        
        // Initialize character counter if available
        const charCounter = document.querySelector('.char-counter');
        if (charCounter && textInput) {
            textInput.addEventListener('input', function() {
                charCounter.textContent = `${this.value.length} characters`;
            });
        }
    }
});

// Main function to analyze text
async function analyzeText() {
    const text = textInput.value.trim();
    
    if (!text) {
        showError('Please enter some text to analyze');
        return;
    }
    
    // Show loading spinner
    loadingSpinner.classList.remove('d-none');
    resultsContainer.classList.add('d-none');
    errorContainer.classList.add('d-none');
    
    try {
        const formData = new FormData();
        formData.append('text', text);
        
        const response = await fetch('/analyze', {
            method: 'POST',
            body: formData
        });
        
        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to analyze text');
        }
        
        const data = await response.json();
        displayResults(data);
    } catch (error) {
        showError(error.message || 'An error occurred during analysis');
    } finally {
        loadingSpinner.classList.add('d-none');
    }
}

// Function to display analysis results
function displayResults(data) {
    // Show results container
    resultsContainer.classList.remove('d-none');
    
    // Update summary section
    const summaryElement = document.getElementById('summary-result');
    summaryElement.textContent = data.summary || 'No summary available';
    
    // Update sentiment visualization
    updateSentimentChart(data.sentiment);
    
    // Update word frequency chart
    updateWordFrequencyChart(data.wordFrequencies);
    
    // Update entities section
    displayEntities(data.entities);
    
    // Update keywords section
    displayKeywords(data.keywords);
}

// Function to update sentiment chart
function updateSentimentChart(sentimentData) {
    const sentimentChartCanvas = document.getElementById('sentiment-chart');
    const ctx = sentimentChartCanvas.getContext('2d');
    
    // Destroy previous chart if it exists
    if (sentimentChart) {
        sentimentChart.destroy();
    }
    
    // Get sentiment scores
    const positive = sentimentData.positive;
    const negative = sentimentData.negative;
    const neutral = sentimentData.neutral;
    
    // Create new chart
    sentimentChart = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Positive', 'Negative', 'Neutral'],
            datasets: [{
                data: [positive, negative, neutral],
                backgroundColor: [
                    'rgba(75, 192, 192, 0.7)',
                    'rgba(255, 99, 132, 0.7)',
                    'rgba(201, 203, 207, 0.7)'
                ],
                borderColor: [
                    'rgb(75, 192, 192)',
                    'rgb(255, 99, 132)',
                    'rgb(201, 203, 207)'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'bottom',
                },
                title: {
                    display: true,
                    text: `Overall Sentiment: ${sentimentData.sentiment.toUpperCase()} (${sentimentData.compound})`
                }
            }
        }
    });
    
    // Update sentiment badge
    const sentimentBadge = document.getElementById('sentiment-badge');
    sentimentBadge.textContent = sentimentData.sentiment.toUpperCase();
    sentimentBadge.className = 'badge rounded-pill';
    
    // Add color based on sentiment
    if (sentimentData.sentiment === 'positive') {
        sentimentBadge.classList.add('bg-success');
    } else if (sentimentData.sentiment === 'negative') {
        sentimentBadge.classList.add('bg-danger');
    } else {
        sentimentBadge.classList.add('bg-secondary');
    }
}

// Function to update word frequency chart
function updateWordFrequencyChart(wordFrequencyData) {
    const wordFreqChartCanvas = document.getElementById('word-freq-chart');
    const ctx = wordFreqChartCanvas.getContext('2d');
    
    // Destroy previous chart if it exists
    if (wordFreqChart) {
        wordFreqChart.destroy();
    }
    
    // Only get top 10 words for better visualization
    const topWords = wordFrequencyData.slice(0, 10);
    
    // Create new chart
    wordFreqChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: topWords.map(item => item.word),
            datasets: [{
                label: 'Word Frequency',
                data: topWords.map(item => item.frequency),
                backgroundColor: 'rgba(54, 162, 235, 0.7)',
                borderColor: 'rgb(54, 162, 235)',
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Frequency'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Words'
                    }
                }
            },
            plugins: {
                legend: {
                    display: false
                },
                title: {
                    display: true,
                    text: 'Top Words by Frequency'
                }
            }
        }
    });
}

// Function to display entities
function displayEntities(entities) {
    const entitiesContainer = document.getElementById('entities-container');
    entitiesContainer.innerHTML = '';
    
    if (!entities || Object.keys(entities).length === 0) {
        entitiesContainer.innerHTML = '<p class="text-muted">No entities detected</p>';
        return;
    }
    
    // Create entity badges for each type
    for (const [entityType, entityList] of Object.entries(entities)) {
        if (entityList.length > 0) {
            const entityTypeDiv = document.createElement('div');
            entityTypeDiv.className = 'mb-2';
            
            const entityTypeTitle = document.createElement('h6');
            entityTypeTitle.className = 'text-muted mb-1';
            entityTypeTitle.textContent = entityType;
            entityTypeDiv.appendChild(entityTypeTitle);
            
            const entityBadgesDiv = document.createElement('div');
            entityBadgesDiv.className = 'd-flex flex-wrap gap-2';
            
            entityList.forEach(entity => {
                const badge = document.createElement('span');
                badge.className = 'badge rounded-pill bg-info';
                badge.textContent = entity;
                entityBadgesDiv.appendChild(badge);
            });
            
            entityTypeDiv.appendChild(entityBadgesDiv);
            entitiesContainer.appendChild(entityTypeDiv);
        }
    }
}

// Function to display keywords
function displayKeywords(keywords) {
    const keywordsContainer = document.getElementById('keywords-container');
    keywordsContainer.innerHTML = '';
    
    if (!keywords || keywords.length === 0) {
        keywordsContainer.innerHTML = '<p class="text-muted">No keywords detected</p>';
        return;
    }
    
    const keywordsList = document.createElement('div');
    keywordsList.className = 'd-flex flex-wrap gap-2';
    
    keywords.forEach(keyword => {
        const badge = document.createElement('span');
        badge.className = 'badge rounded-pill bg-primary';
        badge.textContent = keyword;
        keywordsList.appendChild(badge);
    });
    
    keywordsContainer.appendChild(keywordsList);
}

// Function to show errors
function showError(message) {
    errorContainer.classList.remove('d-none');
    errorContainer.textContent = message;
    resultsContainer.classList.add('d-none');
}

// Helper to get random sample text for demo
function loadSampleText() {
    const sampleTexts = [
        "Climate change is one of the biggest challenges facing our planet today. Rising global temperatures have led to changing weather patterns, rising sea levels, and more frequent natural disasters. Scientists from organizations like NASA and the IPCC have been warning about these effects for decades. Many countries around the world, including the United States, China, and members of the European Union, are now implementing policies to reduce carbon emissions and transition to renewable energy sources such as solar and wind power.",
        
        "Artificial intelligence is transforming industries across the global economy. Companies like Google, Microsoft, and OpenAI are developing sophisticated machine learning models that can understand natural language, recognize images, and even generate creative content. While AI offers tremendous potential benefits in healthcare, education, and scientific research, it also raises important ethical questions about privacy, job displacement, and algorithmic bias that society must address.",
        
        "The COVID-19 pandemic has had profound effects on healthcare systems and economies worldwide. The virus, first identified in Wuhan, China in December 2019, quickly spread across countries like Italy, the United States, and Brazil. Organizations such as the World Health Organization coordinated international responses, while pharmaceutical companies like Pfizer, Moderna, and AstraZeneca developed vaccines in record time. The pandemic also accelerated digital transformation, changing how people work, learn, and access services."
    ];
    
    const randomIndex = Math.floor(Math.random() * sampleTexts.length);
    textInput.value = sampleTexts[randomIndex];
}

// This event listener is now handled in the DOMContentLoaded block above
