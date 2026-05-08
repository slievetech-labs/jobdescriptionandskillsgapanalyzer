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
    page_icon="⛰",
    layout="wide",
)

def read_uploaded_file(uploaded_file):
    if uploaded_file is None:
        return ""
    return uploaded_file.read().decode("utf-8", errors="ignore")


st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #02120d 0%, #041b14 55%, #020b08 100%);
    color: #f0fdf4;
}

.block-container {
    padding-top: 2.5rem;
    max-width: 1180px;
}

.slieve-hero {
    background:
        radial-gradient(circle at top right, rgba(34,197,94,0.18), transparent 30%),
        linear-gradient(135deg, #03120d 0%, #063826 55%, #02120d 100%);
    border: 1px solid rgba(74,222,128,0.18);
    border-radius: 34px;
    padding: 3rem;
    margin-bottom: 2rem;
    box-shadow: 0 30px 90px rgba(0,0,0,0.45);
}

.brand-row {
    display: flex;
    align-items: center;
    gap: 14px;
    margin-bottom: 1.5rem;
}

.brand-logo {
    width: 54px;
    height: 54px;
    border-radius: 16px;
    background: linear-gradient(135deg, #22c55e, #16a34a);
    display: flex;
    align-items: center;
    justify-content: center;
    color: #02120d;
    font-size: 1.6rem;
    font-weight: 900;
}

.brand-text {
    font-size: 1.15rem;
    font-weight: 800;
    color: #bbf7d0;
}

.hero-title {
    font-size: 3.7rem;
    font-weight: 900;
    line-height: 1;
    letter-spacing: -0.07em;
    color: #ffffff;
    margin-bottom: 1rem;
}

.hero-subtitle {
    font-size: 1.1rem;
    line-height: 1.8;
    color: #d1fae5;
    max-width: 760px;
}

.card {
    background: rgba(6,22,17,0.78);
    border: 1px solid rgba(74,222,128,0.10);
    border-radius: 28px;
    padding: 2rem;
    margin-top: 1rem;
    box-shadow: 0 16px 50px rgba(0,0,0,0.30);
}

.stTextArea textarea {
    background: rgba(2,12,9,0.95) !important;
    color: #f0fdf4 !important;
    border: 1px solid rgba(74,222,128,0.18) !important;
    border-radius: 20px !important;
    padding: 1rem !important;
}

.stFileUploader {
    background: rgba(3,15,11,0.75);
    border-radius: 20px;
    padding: 1rem;
    border: 1px dashed rgba(74,222,128,0.22);
}

.stButton button {
    background: linear-gradient(135deg, #22c55e, #15803d);
    color: white;
    border: 0;
    border-radius: 999px;
    padding: 0.85rem 1.8rem;
    font-weight: 800;
    box-shadow: 0 12px 30px rgba(34,197,94,0.22);
}

.stButton button:hover {
    transform: translateY(-2px);
    opacity: 0.96;
}

hr {
    border-color: rgba(74,222,128,0.14);
}

footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)


st.markdown("""
<div class="slieve-hero">
    <div class="brand-row">
        <div class="brand-logo">⌁</div>
        <div class="brand-text">SlieveTech</div>
    </div>

    <div class="hero-title">TalentScope</div>

    <div class="hero-subtitle">
        Enterprise AI intelligence for job descriptions, employment contracts,
        hiring gaps, compliance risks, and workforce alignment analysis.
    </div>
</div>
""", unsafe_allow_html=True)


mode = st.radio(
    "Analysis Mode",
    ["Job Description Review", "Contract Review", "JD Contract Alignment"],
    horizontal=True,
)

st.divider()


if mode == "Job Description Review":
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("Job Description Analysis")

    jd_file = st.file_uploader("Upload JD file", type=["txt"], key="jd_only")
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

    contract_file = st.file_uploader(
        "Upload contract file",
        type=["txt"],
        key="contract_only",
    )
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
            with st.spinner("Analyzing contract clauses..."):
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
            placeholder="Paste the job description...",
        )

    with col2:
        contract_file = st.file_uploader(
            "Upload contract file",
            type=["txt"],
            key="compare_contract",
        )
        contract_text = read_uploaded_file(contract_file)

        contract_text = st.text_area(
            "Paste contract",
            value=contract_text,
            height=350,
            placeholder="Paste the contract...",
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
