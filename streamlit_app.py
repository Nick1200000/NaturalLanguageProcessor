
# import streamlit as st
# from nlp_processor import (
#     analyze_sentiment, 
#     extract_entities, 
#     summarize_text,
#     extract_keywords,
#     get_word_frequencies
# )

# st.set_page_config(page_title="NLP Analyzer", layout="wide")
# st.title("NLP Analyzer")

# # Text input
# text_input = st.text_area("Enter text to analyze", height=200)

# if st.button("Analyze"):
#     if text_input:
#         # Perform analysis
#         sentiment = analyze_sentiment(text_input)
#         entities = extract_entities(text_input)
#         summary = summarize_text(text_input)
#         keywords = extract_keywords(text_input)
#         word_freq = get_word_frequencies(text_input)
        
#         # Display results
#         col1, col2 = st.columns(2)
        
#         with col1:
#             st.subheader("Sentiment Analysis")
#             st.write(f"Compound Score: {sentiment['compound']:.2f}")
#             st.write(f"Positive: {sentiment['pos']:.2f}")
#             st.write(f"Negative: {sentiment['neg']:.2f}")
#             st.write(f"Neutral: {sentiment['neu']:.2f}")
            
#             st.subheader("Named Entities")
#             for entity in entities:
#                 st.write(f"- {entity}")
        
#         with col2:
#             st.subheader("Summary")
#             st.write(summary)
            
#             st.subheader("Keywords")
#             st.write(", ".join(keywords))
            
#         st.subheader("Word Frequencies")
#         st.bar_chart(word_freq)
#     else:
#         st.warning("Please enter some text to analyze.")

import streamlit as st
import os
from nlp_processor import (
    analyze_sentiment, 
    extract_entities, 
    summarize_text,
    extract_keywords,
    get_word_frequencies
)

st.set_page_config(page_title="NLP Analyzer", layout="wide")
st.title("NLP Analyzer")

# Load and render HTML if available
html_path = "templates/index.html"
if os.path.exists(html_path):
    with open(html_path, "r", encoding="utf-8") as file:
        st.markdown(file.read(), unsafe_allow_html=True)
else:
    st.error("HTML file not found! Please check the templates folder.")

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
            if entities:
                for entity in entities:
                    st.write(f"- {entity}")
            else:
                st.write("No named entities detected.")
        
        with col2:
            st.subheader("Summary")
            st.write(summary if summary else "No summary available.")
            
            st.subheader("Keywords")
            st.write(", ".join(keywords) if keywords else "No keywords extracted.")
            
        st.subheader("Word Frequencies")
        if word_freq:
            st.bar_chart(word_freq)
        else:
            st.write("No significant word frequencies detected.")
    else:
        st.warning("Please enter some text to analyze.")

# Footer
st.markdown("---")
st.write("Developed with ❤️ using Streamlit")

