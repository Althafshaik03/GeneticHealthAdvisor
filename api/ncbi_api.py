from Bio import Entrez

Entrez.email = "althafshaik2004@gmail.com"  # Replace with your real email

def fetch_gene_summary(gene_name):
    try:
        search_handle = Entrez.esearch(db="gene", term=gene_name, retmax=1)
        search_results = Entrez.read(search_handle)
        search_handle.close()
        
        if not search_results["IdList"]:
            return "No gene summary found in NCBI."

        gene_id = search_results["IdList"][0]
        fetch_handle = Entrez.efetch(db="gene", id=gene_id, retmode="xml")
        fetch_results = Entrez.read(fetch_handle)
        fetch_handle.close()

        summary = fetch_results[0]["Entrezgene_summary"]
        return summary if summary else "Summary not available."

    except Exception as e:
        return f"⚠️ Error fetching summary: {str(e)}"
