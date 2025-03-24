
import streamlit as st
from nlp_processor import (
    analyze_sentiment, 
    extract_entities, 
    summarize_text,
    extract_keywords,
    get_word_frequencies
)

st.set_page_config(page_title="NLP Analyzer", layout="wide")
st.title("NLP Analyzer")

# Text input
text_input = st.text_area("Enter text to analyze", height=200)

if st.button("Analyze"):
    if text_input:
        # Perform analysis
        sentiment = analyze_sentiment(text_input)
        entities = extract_entities(text_input)
        summary = summarize_text(text_input)
        keywords = extract_keywords(text_input)
        word_freq = get_word_frequencies(text_input)
        
        # Display results
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Sentiment Analysis")
            st.write(f"Compound Score: {sentiment['compound']:.2f}")
            st.write(f"Positive: {sentiment['pos']:.2f}")
            st.write(f"Negative: {sentiment['neg']:.2f}")
            st.write(f"Neutral: {sentiment['neu']:.2f}")
            
            st.subheader("Named Entities")
            for entity in entities:
                st.write(f"- {entity}")
        
        with col2:
            st.subheader("Summary")
            st.write(summary)
            
            st.subheader("Keywords")
            st.write(", ".join(keywords))
            
        st.subheader("Word Frequencies")
        st.bar_chart(word_freq)
    else:
        st.warning("Please enter some text to analyze.")
