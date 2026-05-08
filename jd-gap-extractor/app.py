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
        radial-gradient(circle at top left,
        rgba(34,197,94,0.12),
        transparent 28%),

        linear-gradient(
            180deg,
            #02120d 0%,
            #041b14 50%,
            #03110d 100%
        );

    color: #f0fdf4;
}

/* MAIN */
.block-container {
    padding-top: 2.5rem;
    max-width: 1180px;
}

/* HERO */
.slieve-hero {

    background:
        radial-gradient(circle at top right,
        rgba(74,222,128,0.12),
        transparent 28%),

        linear-gradient(
            135deg,
            rgba(3,20,15,0.96),
            rgba(6,78,59,0.92)
        );

    border: 1px solid rgba(74,222,128,0.16);

    border-radius: 34px;

    padding: 3.2rem;

    box-shadow:
        0 30px 90px rgba(0,0,0,0.45);

    margin-bottom: 2rem;
}

/* BRAND */
.brand-row {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 1.6rem;
}

.brand-logo {
    width: 54px;
    height: 54px;
    border-radius: 16px;

    background:
        linear-gradient(
            135deg,
            #22c55e,
            #16a34a
        );

    display: flex;
    align-items: center;
    justify-content: center;

    color: #02120d;

    font-size: 1.5rem;
    font-weight: 900;

    box-shadow:
        0 10px 30px rgba(34,197,94,0.25);
}

.brand-text {
    font-size: 1.15rem;
    font-weight: 800;
    color: #bbf7d0;
    letter-spacing: -0.02em;
}

/* TITLE */
.hero-title {
    font-size: 3.6rem;
    font-weight: 900;
    line-height: 1;
    letter-spacing: -0.08em;

    background:
        linear-gradient(
            90deg,
            #ffffff,
            #bbf7d0
        );

    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;

    margin-bottom: 1rem;
}

/* SUBTITLE */
.hero-subtitle {
    font-size: 1.1rem;
    line-height: 1.9;
    color: #d1fae5;
    max-width: 760px;
}

/* CARD */
.card {
    background:
        rgba(6,22,17,0.72);

    border:
        1px solid rgba(74,222,128,0.08);

    border-radius: 28px;

    padding: 2rem;

    margin-top: 1rem;

    backdrop-filter: blur(18px);

    box-shadow:
        0 10px 40px rgba(0,0,0,0.25);
}

/* INPUT */
.stTextArea textarea {

    background:
        rgba(2,12,9,0.92) !important;

    color:
        #f0fdf4 !important;

    border:
        1px solid rgba(74,222,128,0.12) !important;

    border-radius: 20px !important;

    padding: 1rem !important;

    font-size: 0.96rem !important;
}

/* UPLOADER */
.stFileUploader {

    background:
        rgba(3,15,11,0.8);

    border-radius: 20px;

    padding: 1rem;

    border:
        1px dashed rgba(74,222,128,0.18);
}

/* BUTTON */
.stButton button {

    background:
        linear-gradient(
            135deg,
            #22c55e,
            #15803d
        );

    color: white;

    border: 0;

    border-radius: 999px;

    padding:
        0.85rem 1.8rem;

    font-weight: 800;

    font-size: 1rem;

    transition: 0.25s ease;

    box-shadow:
        0 12px 30px rgba(34,197,94,0.22);
}

.stButton button:hover {

    transform:
        translateY(-2px);

    opacity: 0.96;
}

/* RADIO */
div[role="radiogroup"] {
    gap: 1rem;
}

/* TABS */
[data-baseweb="tab"] {

    background:
        rgba(255,255,255,0.04);

    border-radius: 14px;

    padding:
        10px 18px;
}

/* SUCCESS */
.stSuccess {

    border-radius: 16px;
}

/* FOOTER */
footer {
    visibility: hidden;
}

</style>


<div class="slieve-hero">

    <div class="brand-row">

        <div class="brand-logo">
            ⛰
        </div>

        <div class="brand-text">
            SlieveTech
        </div>

    </div>

    <div class="hero-title">
        TalentScope
    </div>

    <div class="hero-subtitle">
        Enterprise AI intelligence platform for job descriptions,
        employment contracts, hiring gaps, compliance risks,
        and workforce alignment analysis.
    </div>

</div>

""", unsafe_allow_html=True)

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
