import os
import streamlit as st

os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]

from src.analyzer import (
    analyze_jd_gaps,
    extract_contract_clauses,
    cross_gap_analysis
)

st.set_page_config(
    page_title="TalentScope",
    page_icon="✨",
    layout="wide"
)

# ---------- FILE READER ----------
def read_uploaded_file(uploaded_file):
    if uploaded_file is None:
        return ""
    return uploaded_file.read().decode("utf-8", errors="ignore")


# ---------- PREMIUM UI ----------
st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Inter, sans-serif;
}

.stApp {
    background: #0b1120;
    color: white;
}

.main-container {
    padding-top: 2rem;
}

.hero {
    background:
        linear-gradient(
            135deg,
            rgba(37,99,235,0.18),
            rgba(168,85,247,0.18)
        );
    border: 1px solid rgba(255,255,255,0.08);
    backdrop-filter: blur(18px);
    border-radius: 28px;
    padding: 3rem;
    margin-bottom: 2rem;
}

.hero-title {
    font-size: 3rem;
    font-weight: 800;
    letter-spacing: -1px;
}

.hero-subtitle {
    font-size: 1.1rem;
    opacity: 0.8;
    margin-top: 0.7rem;
}

.card {
    background: rgba(17,24,39,0.75);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 1.5rem;
    margin-top: 1rem;
    backdrop-filter: blur(14px);
}

.stTextArea textarea {
    background: #111827 !important;
    color: white !important;
    border-radius: 18px !important;
    border: 1px solid #374151 !important;
    padding: 1rem !important;
}

.stFileUploader {
    background: rgba(17,24,39,0.65);
    padding: 1rem;
    border-radius: 18px;
    border: 1px dashed rgba(255,255,255,0.15);
}

.stButton button {
    background: linear-gradient(135deg,#2563eb,#7c3aed);
    color: white;
    border: none;
    border-radius: 999px;
    padding: 0.8rem 1.7rem;
    font-weight: 700;
    font-size: 1rem;
}

.stButton button:hover {
    opacity: 0.92;
}

[data-baseweb="tab-list"] {
    gap: 12px;
}

[data-baseweb="tab"] {
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 10px 18px;
}

hr {
    border-color: rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)


# ---------- HERO ----------
st.markdown("""
<div class="hero">
    <div class="hero-title">
        TalentScope
    </div>

    <div class="hero-subtitle">
        Intelligent analysis for job descriptions,
        employment contracts, and hiring alignment.
    </div>
</div>
""", unsafe_allow_html=True)


# ---------- MODE ----------
mode = st.radio(
    "Analysis Mode",
    [
        "Job Description Review",
        "Contract Review",
        "JD Contract Alignment"
    ],
    horizontal=True
)

st.divider()


# ---------- JD ----------
if mode == "Job Description Review":

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Job Description Analysis")

    jd_file = st.file_uploader(
        "Upload JD file",
        type=["txt"],
        key="jd_only"
    )

    jd_text = read_uploaded_file(jd_file)

    jd_text = st.text_area(
        "Or paste job description",
        value=jd_text,
        height=320
    )

    if st.button("Run Analysis"):

        if not jd_text.strip():
            st.warning("Please upload or paste a job description.")

        else:
            with st.spinner("Analyzing..."):
                result = analyze_jd_gaps(jd_text)

            st.success("Analysis completed")
            st.markdown(result)

    st.markdown('</div>', unsafe_allow_html=True)


# ---------- CONTRACT ----------
elif mode == "Contract Review":

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Employment Contract Analysis")

    contract_file = st.file_uploader(
        "Upload contract file",
        type=["txt"],
        key="contract_only"
    )

    contract_text = read_uploaded_file(contract_file)

    contract_text = st.text_area(
        "Or paste contract",
        value=contract_text,
        height=320
    )

    if st.button("Review Contract"):

        if not contract_text.strip():
            st.warning("Please upload or paste a contract.")

        else:
            with st.spinner("Analyzing contract..."):
                result = extract_contract_clauses(contract_text)

            st.success("Contract review completed")
            st.json(result)

    st.markdown('</div>', unsafe_allow_html=True)


# ---------- COMPARISON ----------
else:

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("JD and Contract Alignment")

    col1, col2 = st.columns(2)

    with col1:

        jd_file = st.file_uploader(
            "Upload JD file",
            type=["txt"],
            key="compare_jd"
        )

        jd_text = read_uploaded_file(jd_file)

        jd_text = st.text_area(
            "Paste job description",
            value=jd_text,
            height=350
        )

    with col2:

        contract_file = st.file_uploader(
            "Upload contract file",
            type=["txt"],
            key="compare_contract"
        )

        contract_text = read_uploaded_file(contract_file)

        contract_text = st.text_area(
            "Paste contract",
            value=contract_text,
            height=350
        )

    if st.button("Compare Documents"):

        if not jd_text.strip() or not contract_text.strip():

            st.warning("Please provide both documents.")

        else:

            with st.spinner("Running analysis..."):

                jd_result = analyze_jd_gaps(jd_text)

                contract_result = extract_contract_clauses(contract_text)

                final_result = cross_gap_analysis(
                    jd_result,
                    contract_result
                )

            st.success("Comparison completed")

            tab1, tab2, tab3 = st.tabs([
                "JD Analysis",
                "Contract Clauses",
                "Alignment Report"
            ])

            with tab1:
                st.markdown(jd_result)

            with tab2:
                st.json(contract_result)

            with tab3:
                st.markdown(final_result)

    st.markdown('</div>', unsafe_allow_html=True)


st.divider()

st.caption("TalentScope • AI Hiring Intelligence Platform")
