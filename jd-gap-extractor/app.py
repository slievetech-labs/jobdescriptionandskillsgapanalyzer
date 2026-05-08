import os
import streamlit as st

# =========================
# LOAD SECRET
# =========================
os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]

from src.analyzer import (
    analyze_jd_gaps,
    extract_contract_clauses,
    cross_gap_analysis
)

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="TalentScope",
    page_icon="✦",
    layout="wide"
)

# =========================
# FILE READER
# =========================
def read_uploaded_file(uploaded_file):
    if uploaded_file is None:
        return ""
    return uploaded_file.read().decode("utf-8", errors="ignore")


# =========================
# CUSTOM SLIEVE TECH UI
# =========================
st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Inter, sans-serif;
}

.stApp {
    background:
        linear-gradient(
            180deg,
            #07111f 0%,
            #0b1726 100%
        );
    color: #f8fafc;
}

/* MAIN CONTAINER */
.block-container {
    padding-top: 3rem;
    max-width: 1180px;
}

/* HERO */
.slieve-hero {
    background:
        radial-gradient(circle at top left,
        rgba(14,165,233,0.22),
        transparent 35%),

        linear-gradient(
            135deg,
            #0f172a 0%,
            #111827 55%,
            #0c4a6e 100%
        );

    border: 1px solid rgba(125,211,252,0.16);
    border-radius: 30px;
    padding: 3rem;
    box-shadow: 0 30px 80px rgba(0,0,0,0.45);
    margin-bottom: 2rem;
}

.brand-kicker {
    color: #38bdf8;
    font-size: 0.82rem;
    font-weight: 800;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.hero-title {
    font-size: 3.5rem;
    font-weight: 900;
    letter-spacing: -0.07em;
    margin-bottom: 1rem;
    line-height: 1;
}

.hero-subtitle {
    color: #cbd5e1;
    font-size: 1.15rem;
    line-height: 1.8;
    max-width: 760px;
}

/* CARD */
.card {
    background: rgba(15,23,42,0.82);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 26px;
    padding: 2rem;
    margin-top: 1rem;
    box-shadow: 0 12px 50px rgba(0,0,0,0.28);
    backdrop-filter: blur(18px);
}

/* TEXTAREA */
.stTextArea textarea {
    background: #0f172a !important;
    color: #f8fafc !important;
    border: 1px solid rgba(125,211,252,0.16) !important;
    border-radius: 18px !important;
    padding: 1rem !important;
    font-size: 0.96rem !important;
}

/* FILE UPLOADER */
.stFileUploader {
    background: rgba(15,23,42,0.72);
    border-radius: 18px;
    padding: 1rem;
    border: 1px dashed rgba(125,211,252,0.18);
}

/* BUTTON */
.stButton button {
    background:
        linear-gradient(
            135deg,
            #0284c7,
            #0f766e
        );

    color: white;
    border: 0;
    border-radius: 999px;
    padding: 0.8rem 1.6rem;
    font-weight: 800;
    font-size: 1rem;
    transition: 0.2s ease;
}

.stButton button:hover {
    transform: translateY(-1px);
    opacity: 0.95;
}

/* RADIO */
div[role="radiogroup"] {
    gap: 1rem;
}

/* TABS */
[data-baseweb="tab-list"] {
    gap: 12px;
}

[data-baseweb="tab"] {
    background: rgba(255,255,255,0.05);
    border-radius: 12px;
    padding: 10px 18px;
}

/* DIVIDER */
hr {
    border-color: rgba(255,255,255,0.08);
}

/* SUCCESS */
.stSuccess {
    border-radius: 18px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HERO SECTION
# =========================
st.markdown("""
<div class="slieve-hero">

    <div class="brand-kicker">
        Slieve Tech
    </div>

    <div class="hero-title">
        TalentScope
    </div>

    <div class="hero-subtitle">
        Premium AI intelligence platform for job descriptions,
        employment contracts, hiring gaps, legal risks,
        and candidate-role alignment analysis.
    </div>

</div>
""", unsafe_allow_html=True)

# =========================
# MODE SELECTION
# =========================
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

# =========================
# JD MODE
# =========================
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
        height=320,
        placeholder="Paste the job description here..."
    )

    if st.button("Run Analysis"):

        if not jd_text.strip():

            st.warning("Please upload or paste a job description.")

        else:

            with st.spinner("Analyzing job description..."):

                result = analyze_jd_gaps(jd_text)

            st.success("Analysis completed")

            st.markdown(result)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# CONTRACT MODE
# =========================
elif mode == "Contract Review":

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("Employment Contract Review")

    contract_file = st.file_uploader(
        "Upload contract file",
        type=["txt"],
        key="contract_only"
    )

    contract_text = read_uploaded_file(contract_file)

    contract_text = st.text_area(
        "Or paste employment contract",
        value=contract_text,
        height=320,
        placeholder="Paste the employment contract here..."
    )

    if st.button("Review Contract"):

        if not contract_text.strip():

            st.warning("Please upload or paste a contract.")

        else:

            with st.spinner("Analyzing contract clauses..."):

                result = extract_contract_clauses(contract_text)

            st.success("Contract review completed")

            st.json(result)

    st.markdown('</div>', unsafe_allow_html=True)

# =========================
# COMPARISON MODE
# =========================
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
            height=350,
            placeholder="Paste the job description..."
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
            height=350,
            placeholder="Paste the contract..."
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

# =========================
# FOOTER
# =========================
st.divider()

st.caption("TalentScope • Built by Slieve Tech")
