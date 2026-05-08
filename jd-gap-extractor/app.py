import streamlit as st
from anthropic import Anthropic
from src.analyzer import analyze_jd_gaps

client = Anthropic(
    api_key=st.secrets["ANTHROPIC_API_KEY"]
)

st.title("JD Gap Analyzer")

jd_text = st.text_area("Paste Job Description")

if st.button("Analyze"):
    if jd_text.strip():
        result = analyze_jd_gaps(jd_text)
        st.write(result)
    else:
        st.warning("Please enter a job description.")
