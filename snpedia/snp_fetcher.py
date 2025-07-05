import requests
from bs4 import BeautifulSoup

def fetch_snp_summary(rsid):
    base_url = f"https://www.snpedia.com/index.php/{rsid}"
    try:
        resp = requests.get(base_url, timeout=10)
        soup = BeautifulSoup(resp.text, "html.parser")

        content = soup.find("div", {"id": "mw-content-text"})
        if not content:
            return "No content found for this SNP."

        paras = content.find_all("p")
        summary = "\n\n".join(p.get_text().strip() for p in paras if len(p.get_text().strip()) > 20)

        if summary:
            return summary.strip()
        return f"No detailed info found for {rsid}."
    except Exception as e:
        return f"⚠️ Error fetching {rsid}: {str(e)}"
