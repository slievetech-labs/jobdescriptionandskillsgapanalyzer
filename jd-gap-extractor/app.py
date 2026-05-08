import os
import streamlit as st

# Load Streamlit secret into environment
os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]

from src.analyzer import analyze_jd_gaps

st.title("JD Gap Analyzer")

jd_text = st.text_area("Paste Job Description")

if st.button("Analyze"):
    if jd_text.strip():
        result = analyze_jd_gaps(jd_text)
        st.write(result)
    else:
        st.warning("Please enter a job description.")
