import os
import streamlit as st

os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]

from src.analyzer import analyze_jd_gaps, extract_contract_clauses, cross_gap_analysis

st.set_page_config(
    page_title="JD Gap Analyzer",
    page_icon="🧠",
    layout="wide"
)

st.markdown("""
<style>
.main {
    background-color: #0f172a;
}
.block-container {
    padding-top: 3rem;
    padding-bottom: 3rem;
}
.hero {
    background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
    padding: 2rem;
    border-radius: 24px;
    color: white;
    margin-bottom: 2rem;
}
.card {
    background: #111827;
    border: 1px solid #374151;
    border-radius: 20px;
    padding: 1.5rem;
    margin-bottom: 1rem;
}
.stTextArea textarea {
    border-radius: 16px;
}
.stButton button {
    border-radius: 999px;
    padding: 0.6rem 1.5rem;
    font-weight: 700;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
    <h1>🧠 JD Gap Analyzer</h1>
    <p>Analyze job descriptions, review employment contracts, and compare both for gaps, risks, and mismatches.</p>
</div>
""", unsafe_allow_html=True)

mode = st.radio(
    "Choose analysis mode",
    [
        "JD only",
        "Contract only",
        "Compare JD + Contract"
    ],
    horizontal=True
)

st.divider()

if mode == "JD only":
    st.subheader("📄 Job Description Analysis")

    jd_text = st.text_area(
        "Paste job description",
        height=300,
        placeholder="Paste the job description here..."
    )

    if st.button("Analyze JD"):
        if not jd_text.strip():
            st.warning("Please paste a job description.")
        else:
            with st.spinner("Analyzing job description..."):
                result = analyze_jd_gaps(jd_text)
            st.success("Analysis complete")
            st.markdown(result)

elif mode == "Contract only":
    st.subheader("📑 Contract Clause Extraction")

    contract_text = st.text_area(
        "Paste employment contract",
        height=300,
        placeholder="Paste the employment contract here..."
    )

    if st.button("Analyze Contract"):
        if not contract_text.strip():
            st.warning("Please paste a contract.")
        else:
            with st.spinner("Analyzing contract..."):
                result = extract_contract_clauses(contract_text)
            st.success("Analysis complete")
            st.json(result)

else:
    st.subheader("⚖️ JD vs Contract Comparison")

    col1, col2 = st.columns(2)

    with col1:
        jd_text = st.text_area(
            "Paste job description",
            height=350,
            placeholder="Paste the job description here..."
        )

    with col2:
        contract_text = st.text_area(
            "Paste employment contract",
            height=350,
            placeholder="Paste the employment contract here..."
        )

    if st.button("Compare JD + Contract"):
        if not jd_text.strip() or not contract_text.strip():
            st.warning("Please paste both the job description and contract.")
        else:
            with st.spinner("Analyzing JD..."):
                jd_result = analyze_jd_gaps(jd_text)

            with st.spinner("Extracting contract clauses..."):
                contract_result = extract_contract_clauses(contract_text)

            with st.spinner("Comparing JD and contract..."):
                final_result = cross_gap_analysis(jd_result, contract_result)

            st.success("Comparison complete")

            tab1, tab2, tab3 = st.tabs([
                "JD Analysis",
                "Contract Clauses",
                "Cross-Gap Report"
            ])

            with tab1:
                st.markdown(jd_result)

            with tab2:
                st.json(contract_result)

            with tab3:
                st.markdown(final_result)

st.divider()

st.caption("Powered by Streamlit + Anthropic Claude")
