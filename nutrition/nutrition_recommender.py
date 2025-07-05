import json
import pandas as pd

def load_snp_rules():
    with open("nutrition/snp_rules.json", "r") as f:
        return json.load(f)

def process_snp_file(uploaded_file):
    snp_data = pd.read_csv(uploaded_file)
    rules = load_snp_rules()
    recommendations = []

    for _, row in snp_data.iterrows():
        rsid = row["rsID"]
        genotype = row["Genotype"]
        if rsid in rules and genotype in rules[rsid]:
            recommendations.append(rules[rsid][genotype])

    return recommendations
