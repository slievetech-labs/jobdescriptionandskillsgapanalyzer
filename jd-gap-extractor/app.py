import os
import streamlit as st

os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]

from src.analyzer import (
    analyze_jd_gaps,
    extract_contract_clauses,
    cross_gap_analysis,
)

st.set_page_config(
    page_title="TalentScope | SlieveTech",
    page_icon="▲",
    layout="wide",
)

def read_uploaded_file(uploaded_file):
    if uploaded_file is None:
        return ""
    return uploaded_file.read().decode("utf-8", errors="ignore")


st.markdown(
"""
<style>
.stApp {
    background: #03110c;
    color: #f0fdf4;
}

.block-container {
    max-width: 1180px;
    padding-top: 2.5rem;
}

.hero {
    background: linear-gradient(135deg, #03110c 0%, #063f2a 100%);
    border: 1px solid rgba(34,197,94,0.25);
    border-radius: 32px;
    padding: 3rem;
    margin-bottom: 2rem;
    box-shadow: 0 30px 90px rgba(0,0,0,0.45);
}

.logo-row {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 2rem;
}

.logo-box {
    width: 52px;
    height: 52px;
    border-radius: 14px;
    background: #00e676;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #03110c;
    font-weight: 900;
    font-size: 24px;
}

.logo-text {
    font-size: 1.25rem;
    font-weight: 900;
    color: #ffffff;
}

.logo-text span {
    color: #00e676;
}

.hero-title {
    font-size: 4rem;
    font-weight: 950;
    letter-spacing: -0.08em;
    line-height: 1;
    color: #ffffff;
    margin-bottom: 1rem;
}

.hero-subtitle {
    color: #bbf7d0;
    font-size: 1.15rem;
    line-height: 1.8;
    max-width: 720px;
}

.card {
    background: rgba(2,18,13,0.95);
    border: 1px solid rgba(34,197,94,0.18);
    border-radius: 28px;
    padding: 2rem;
    margin-top: 1.5rem;
}

.stTextArea textarea {
    background: #020c09 !important;
    color: #f0fdf4 !important;
    border: 1px solid rgba(34,197,94,0.22) !important;
    border-radius: 18px !important;
}

.stFileUploader {
    background: rgba(2,18,13,0.85);
    border: 1px dashed rgba(34,197,94,0.28);
    border-radius: 18px;
    padding: 1rem;
}

.stButton button {
    background: #00c853;
    color: #03110c;
    border: none;
    border-radius: 999px;
    padding: 0.8rem 1.8rem;
    font-weight: 900;
}

.stButton button:hover {
    background: #00e676;
    color: #03110c;
}

hr {
    border-color: rgba(34,197,94,0.18);
}

footer {
    visibility: hidden;
}
</style>

<div class="hero">
    <div class="logo-row">
        <div class="logo-box">⌁</div>
        <div class="logo-text">Slieve<span>Tech</span></div>
    </div>

    <div class="hero-title">TalentScope</div>

    <div class="hero-subtitle">
        AI-powered analysis for job descriptions, employment contracts,
        hiring gaps, compliance risks, and workforce alignment.
    </div>
</div>
""",
unsafe_allow_html=True
)


mode = st.radio(
    "Analysis Mode",
    ["Job Description Review", "Contract Review", "JD Contract Alignment"],
    horizontal=True,
)

st.divider()


if mode == "Job Description Review":
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Job Description Analysis")

    jd_file = st.file_uploader("Upload JD file", type=["txt"], key="jd_file")
    jd_text = read_uploaded_file(jd_file)

    jd_text = st.text_area(
        "Or paste job description",
        value=jd_text,
        height=320,
        placeholder="Paste the job description here...",
    )

    if st.button("Run Analysis"):
        if not jd_text.strip():
            st.warning("Please upload or paste a job description.")
        else:
            with st.spinner("Analyzing job description..."):
                result = analyze_jd_gaps(jd_text)
            st.success("Analysis completed")
            st.markdown(result)

    st.markdown("</div>", unsafe_allow_html=True)


elif mode == "Contract Review":
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Employment Contract Review")

    contract_file = st.file_uploader("Upload contract file", type=["txt"], key="contract_file")
    contract_text = read_uploaded_file(contract_file)

    contract_text = st.text_area(
        "Or paste employment contract",
        value=contract_text,
        height=320,
        placeholder="Paste the employment contract here...",
    )

    if st.button("Review Contract"):
        if not contract_text.strip():
            st.warning("Please upload or paste a contract.")
        else:
            with st.spinner("Analyzing contract..."):
                result = extract_contract_clauses(contract_text)
            st.success("Contract review completed")
            st.json(result)

    st.markdown("</div>", unsafe_allow_html=True)


else:
    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("JD and Contract Alignment")

    col1, col2 = st.columns(2)

    with col1:
        jd_file = st.file_uploader("Upload JD file", type=["txt"], key="compare_jd")
        jd_text = read_uploaded_file(jd_file)

        jd_text = st.text_area(
            "Paste job description",
            value=jd_text,
            height=350,
        )

    with col2:
        contract_file = st.file_uploader("Upload contract file", type=["txt"], key="compare_contract")
        contract_text = read_uploaded_file(contract_file)

        contract_text = st.text_area(
            "Paste contract",
            value=contract_text,
            height=350,
        )

    if st.button("Compare Documents"):
        if not jd_text.strip() or not contract_text.strip():
            st.warning("Please provide both documents.")
        else:
            with st.spinner("Analyzing job description..."):
                jd_result = analyze_jd_gaps(jd_text)

            with st.spinner("Reviewing contract..."):
                contract_result = extract_contract_clauses(contract_text)

            with st.spinner("Generating alignment report..."):
                final_result = cross_gap_analysis(jd_result, contract_result)

            st.success("Comparison completed")

            tab1, tab2, tab3 = st.tabs(
                ["JD Analysis", "Contract Clauses", "Alignment Report"]
            )

            with tab1:
                st.markdown(jd_result)

            with tab2:
                st.json(contract_result)

            with tab3:
                st.markdown(final_result)

    st.markdown("</div>", unsafe_allow_html=True)


st.divider()
st.caption("TalentScope • Built by SlieveTech")
