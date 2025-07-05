import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
from chatbot.chatbot import match_disease
from nutrition.nutrition_recommender import process_snp_file
from nutrition.ml_model import predict_from_model
from utils.fasta_converter_stream import convert_fasta_to_csv, convert_fastq_to_csv
from api.ncbi_api import fetch_gene_summary
from snpedia.snp_fetcher import fetch_snp_summary
from utils.pdf_report import generate_disease_pdf
import pandas as pd

# Must be the first Streamlit command
st.set_page_config(page_title="Genetic Health Advisor", layout="wide")

# App styling
st.markdown("""
    <style>
    .main {background-color: #f8fbff;}
    .block-container {padding-top: 2rem;}
    .css-18e3th9 {padding: 2rem 1rem;}
    .stTabs [data-baseweb="tab"] {
        font-size: 1.1rem;
        padding: 0.6rem 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.image("https://upload.wikimedia.org/wikipedia/commons/2/2f/DNA_helix_structure.png", use_column_width=True)
    st.markdown("## 🧬 Genetic Health Advisor")
    st.markdown("Navigate using the tabs:")
    st.markdown("- 💬 Chatbot for diseases\n- 🧪 SNP dietary advisor\n- 📄 FASTA sequence parser\n- 🔍 NCBI gene summaries\n- 🔍 SNPedia Lookup")
    st.markdown("---")
    st.caption("Developed by [Your Name], 2025")

st.title("🧬 AI-Powered Genetic Health Advisor")

# Tab layout
chatbot_tab, snp_tab, fasta_tab, ncbi_tab, snpedia_tab = st.tabs([
    "💬 Disease Chatbot",
    "🥗 SNP Recommender",
    "📄 FASTA/FASTQ",
    "🔬 Gene Info (NCBI)",
    "🔍 SNP Lookup (SNPedia)"
])

# -------------------- Chatbot ---------------------
with chatbot_tab:
    st.subheader("Genetic Disease Info (Multilingual Support)")
    query = st.text_input("Enter disease name or symptoms")
    lang = st.selectbox("Language", ["en", "hi", "kn"], index=0)

    if st.button("Search"):
        result = match_disease(query, lang)
        st.text_area("Response", result, height=250)

        # PDF generation option
        if result and query:
            st.markdown("📄 Generate a downloadable report:")
            if st.button("Download Report as PDF"):
                pdf_bytes = generate_disease_pdf(query, result)
                st.download_button(
                    label="📥 Download PDF",
                    data=pdf_bytes,
                    file_name=f"disease_report_{query.replace(' ', '_')}.pdf",
                    mime="application/pdf"
                )

# -------------------- SNP Nutrition ---------------------
with snp_tab:
    st.subheader("Upload SNP CSV File")
    use_model = st.checkbox("Use AI Model for Prediction", value=True)
    snp_file = st.file_uploader("Upload your SNP profile CSV", type=["csv"])

    if snp_file and st.button("Get Nutrition Advice"):
        snp_df = pd.read_csv(snp_file).set_index("rsID").T

        if use_model:
            prediction = predict_from_model(snp_df)
            st.success(f"🧠 AI Prediction: {prediction}")
        else:
            recommendations = process_snp_file(snp_file)
            for item in recommendations:
                st.info(item)

# -------------------- FASTA / FASTQ ---------------------
with fasta_tab:
    st.subheader("Convert FASTA or FASTQ to CSV with DNA Properties")
    file_uploaded = st.file_uploader("Upload a FASTA (.fasta) or FASTQ (.fastq) file", type=["fasta", "fa", "fastq", "fq"])
    show_props = st.checkbox("Calculate GC%, Melting Temp, MW", value=True)

    if file_uploaded:
        file_ext = file_uploaded.name.split(".")[-1].lower()
        file_data = file_uploaded.getvalue().decode("utf-8").splitlines()
        if file_ext in ["fasta", "fa"]:
            df = convert_fasta_to_csv(file_data, compute_properties=show_props)
        elif file_ext in ["fastq", "fq"]:
            df = convert_fastq_to_csv(file_uploaded, compute_properties=show_props)
        else:
            st.error("Unsupported file format.")
            df = None

        if df is not None:
            st.dataframe(df)
            st.download_button("Download CSV", df.to_csv(index=False).encode("utf-8"), "converted_sequences.csv", "text/csv")
        if df is not None and show_props:
            st.subheader("🔬 DNA Sequence Insights")
            st.bar_chart(df[["Length", "GC(%)", "Melting Temp"]].set_index(df["Name"]))

# -------------------- NCBI Gene Info ---------------------
with ncbi_tab:
    st.subheader("Search Real-Time Gene Summary from NCBI")
    gene_query = st.text_input("Enter gene symbol (e.g., BRCA1, CFTR, PAH)")
    if st.button("Fetch Summary"):
        summary = fetch_gene_summary(gene_query)
        st.text_area("NCBI Summary", summary, height=250)

# -------------------- SNPedia Lookup ---------------------
with snpedia_tab:
    st.subheader("🔍 Real-Time SNP Insights from SNPedia")
    rsid = st.text_input("Enter SNP ID (e.g., rs1801133, rs9939609):")

    if rsid:
        with st.spinner("Fetching summary from SNPedia..."):
            summary = fetch_snp_summary(rsid.strip())
        st.markdown("#### 📄 SNPedia Summary")
        st.text_area("SNP Description", summary, height=300)
        st.caption(f"🔗 [View on SNPedia](https://www.snpedia.com/index.php/{rsid.strip()})")
