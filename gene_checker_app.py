# Gene Checker Interactive App
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Gene Checker", layout="centered")

st.title("Gene Checker for ADHD, Autism, Fibromyalgia, Bipolar")

st.markdown("""
Upload your **gene panel CSV** (one column with gene symbols) and get a report of which condition(s) each gene is associated with, plus links to NCBI, PharmGKB, and ClinGen.
""")

# Upload file
uploaded_file = st.file_uploader("Upload CSV or TXT", type=["csv", "txt"])

# Example condition-specific genes
conditions_genes = {
    "ADHD": {"DRD4", "SLC6A3", "COMT", "SNAP25", "ADRA2A"},
    "Autism": {"SHANK3", "MECP2", "NRXN1", "CHD8", "FMR1"},
    "Fibromyalgia": {"SLC6A4", "TRPV1", "COMT", "TNF", "IL6"},
    "Bipolar": {"BDNF", "CACNA1C", "ANK3", "NCAN", "CACNB2"},
    "Other": {"GENE1", "GENE2"}  # placeholder
}

def process_gene_panel(gene_list):
    results = []
    for gene in gene_list:
        associated = [cond for cond, genes in conditions_genes.items() if gene in genes]
        if not associated:
            associated = ["Unknown"]
        results.append({
            "Gene": gene,
            "Condition(s)": ", ".join(associated),
            "NCBI": f"https://www.ncbi.nlm.nih.gov/gene/?term={gene}",
            "PharmGKB": f"https://www.pharmgkb.org/search?query={gene}",
            "ClinGen": f"https://clinicalgenome.org/search/?search={gene}"
        })
    return pd.DataFrame(results)

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith(".csv"):
            df_input = pd.read_csv(uploaded_file)
        else:
            df_input = pd.read_csv(uploaded_file, header=None)
            df_input.columns = ["Gene"]
        gene_list = df_input.iloc[:,0].astype(str).str.strip().tolist()
        df_results = process_gene_panel(gene_list)
        st.subheader("Gene Report")
        st.dataframe(df_results)
        csv = df_results.to_csv(index=False)
        st.download_button(
            label=" Download Report as CSV",
            data=csv,
            file_name="gene_report.csv",
            mime="text/csv"
        )
    except Exception as e:
        st.error(f"Error reading file: {e}")
else:
    st.info("Upload a CSV or TXT file with one column containing gene symbols.")
