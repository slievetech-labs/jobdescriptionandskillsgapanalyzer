import os
import streamlit as st

# =========================
# API KEY
# =========================

os.environ["ANTHROPIC_API_KEY"] = st.secrets["ANTHROPIC_API_KEY"]

# =========================
# IMPORTS
# =========================

from src.analyzer import (
    analyze_jd_gaps,
    extract_contract_clauses,
    cross_gap_analysis,
)

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="TalentScope | SlieveTech",
    page_icon=None,
    layout="wide",
)

# =========================
# HELPERS
# =========================

def read_uploaded_file(uploaded_file):
    if uploaded_file is None:
        return ""

    return uploaded_file.read().decode(
        "utf-8",
        errors="ignore"
    )

# =========================
# PREMIUM SLIEVETECH THEME
# =========================

st.markdown("""
<style>

/* GLOBAL */

html, body, [class*="css"] {
    font-family: Inter, sans-serif;
}

/* BACKGROUND */

.stApp {

    background:
        radial-gradient(
            circle at top left,
            rgba(0,255,136,0.08),
            transparent 28%
        ),

        linear-gradient(
            180deg,
            #02120d 0%,
            #041b14 55%,
            #020b08 100%
        );

    color: #f0fdf4;
}

/* PAGE WIDTH */

.block-container {
    max-width: 1180px;
    padding-top: 2.2rem;
}

/* HERO */

.hero {

    background:
        radial-gradient(
            circle at top right,
            rgba(0,255,136,0.10),
            transparent 30%
        ),

        linear-gradient(
            135deg,
            #03140f 0%,
            #063b29 100%
        );

    border:
        1px solid rgba(0,255,140,0.18);

    border-radius: 34px;

    padding: 3rem;

    margin-bottom: 2.5rem;

    box-shadow:
        0 25px 80px rgba(0,0,0,0.42);
}

/* BRAND */

.logo-row {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 1.8rem;
}

.logo-box {

    width: 60px;
    height: 60px;

    border-radius: 18px;

    background:
        linear-gradient(
            135deg,
            #00ff88,
            #00c853
        );

    display: flex;
    align-items: center;
    justify-content: center;

    color: #02120d;

    font-size: 1.5rem;
    font-weight: 900;

    box-shadow:
        0 10px 30px rgba(0,255,136,0.25);
}

.logo-text {

    font-size: 1.4rem;
    font-weight: 900;
    color: white;
}

.logo-text span {
    color: #00ff88;
}

/* TITLE */

.hero-title {

    font-size: 4.8rem;

    font-weight: 950;

    line-height: 1;

    letter-spacing: -0.08em;

    color: white;

    margin-bottom: 1rem;
}

/* SUBTITLE */

.hero-subtitle {

    font-size: 1.12rem;

    color: #d1fae5;

    line-height: 1.9;

    max-width: 760px;
}

/* ANALYSIS CARDS */

.card {

    background:
        rgba(3,17,12,0.82);

    border:
        1px solid rgba(0,255,140,0.10);

    border-radius: 28px;

    padding: 2rem;

    margin-top: 1.5rem;

    box-shadow:
        0 10px 40px rgba(0,0,0,0.25);
}

/* TEXTAREA */

.stTextArea textarea {

    background:
        rgba(2,12,9,0.96) !important;

    color:
        #f0fdf4 !important;

    border:
        1px solid rgba(0,255,140,0.14) !important;

    border-radius: 18px !important;

    padding: 1rem !important;

    font-size: 0.97rem !important;
}

/* FILE UPLOADER */

.stFileUploader {

    background:
        rgba(2,18,13,0.85);

    border:
        1px dashed rgba(0,255,140,0.18);

    border-radius: 18px;

    padding: 1rem;
}

/* BUTTON */

.stButton button {

    background:
        linear-gradient(
            135deg,
            #00ff88,
            #00c853
        );

    color: #02120d;

    border: none;

    border-radius: 999px;

    padding:
        0.82rem 1.8rem;

    font-weight: 900;

    transition: 0.25s ease;

    box-shadow:
        0 10px 30px rgba(0,255,136,0.22);
}

.stButton button:hover {

    transform:
        translateY(-2px);

    opacity: 0.96;
}

/* RADIO BUTTONS */

div[role="radiogroup"] {
    gap: 1rem;
}

/* DIVIDER */

hr {
    border-color: rgba(0,255,140,0.12);
}

/* REMOVE STREAMLIT BRANDING */

footer {
    visibility: hidden;
}

#MainMenu {
    visibility: hidden;
}

header {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HERO SECTION
# =========================

st.html("""
<div class="hero">

    

    <div class="hero-title">
        TalentScope
    </div>

    <div class="hero-subtitle">
        AI-powered enterprise intelligence for job descriptions,
        employment contracts, hiring gaps, compliance risks,
        and workforce alignment analysis.
    </div>

</div>
""")

# =========================
# MODE SELECTOR
# =========================

mode = st.radio(
    "Analysis Mode",
    [
        "Job Description Review",
        "Contract Review",
        "JD Contract Alignment"
    ],
    horizontal=True,
)

st.divider()

# =========================
# JOB DESCRIPTION REVIEW
# =========================

if mode == "Job Description Review":

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.subheader("Job Description Analysis")

    jd_file = st.file_uploader(
        "Upload JD File",
        type=["txt"],
        key="jd_file"
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

            st.warning(
                "Please upload or paste a job description."
            )

        else:

            with st.spinner(
                "Analyzing job description..."
            ):

                result = analyze_jd_gaps(jd_text)

            st.success("Analysis completed")

            st.markdown(result)

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

# =========================
# CONTRACT REVIEW
# =========================

elif mode == "Contract Review":

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.subheader("Employment Contract Review")

    contract_file = st.file_uploader(
        "Upload Contract File",
        type=["txt"],
        key="contract_file"
    )

    contract_text = read_uploaded_file(
        contract_file
    )

    contract_text = st.text_area(
        "Or paste employment contract",
        value=contract_text,
        height=320,
        placeholder="Paste the contract here..."
    )

    if st.button("Review Contract"):

        if not contract_text.strip():

            st.warning(
                "Please upload or paste a contract."
            )

        else:

            with st.spinner(
                "Reviewing contract..."
            ):

                result = extract_contract_clauses(
                    contract_text
                )

            st.success(
                "Contract review completed"
            )

            st.json(result)

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

# =========================
# JD CONTRACT ALIGNMENT
# =========================

else:

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.subheader(
        "JD and Contract Alignment"
    )

    col1, col2 = st.columns(2)

    # LEFT COLUMN

    with col1:

        jd_file = st.file_uploader(
            "Upload JD File",
            type=["txt"],
            key="compare_jd"
        )

        jd_text = read_uploaded_file(
            jd_file
        )

        jd_text = st.text_area(
            "Paste job description",
            value=jd_text,
            height=350,
            placeholder="Paste job description..."
        )

    # RIGHT COLUMN

    with col2:

        contract_file = st.file_uploader(
            "Upload Contract File",
            type=["txt"],
            key="compare_contract"
        )

        contract_text = read_uploaded_file(
            contract_file
        )

        contract_text = st.text_area(
            "Paste contract",
            value=contract_text,
            height=350,
            placeholder="Paste employment contract..."
        )

    # ANALYZE BUTTON

    if st.button("Compare Documents"):

        if (
            not jd_text.strip()
            or
            not contract_text.strip()
        ):

            st.warning(
                "Please provide both documents."
            )

        else:

            with st.spinner(
                "Analyzing job description..."
            ):

                jd_result = analyze_jd_gaps(
                    jd_text
                )

            with st.spinner(
                "Reviewing contract..."
            ):

                contract_result = (
                    extract_contract_clauses(
                        contract_text
                    )
                )

            with st.spinner(
                "Generating alignment report..."
            ):

                final_result = (
                    cross_gap_analysis(
                        jd_result,
                        contract_result
                    )
                )

            st.success(
                "Comparison completed"
            )

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

    st.markdown(
        "</div>",
        unsafe_allow_html=True
    )

# =========================
# FOOTER
# =========================

st.divider()

st.caption(
    "TalentScope • Built by SlieveTech"
)
