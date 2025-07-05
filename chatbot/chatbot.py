import os
import pandas as pd
import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from utils.advanced_translate import IndicTranslator

# Initialize the multilingual translator
translator = IndicTranslator()

# Load spaCy NLP model
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    raise ImportError("SpaCy model 'en_core_web_sm' not found. Install it with:\npython -m spacy download en_core_web_sm")

# Load the disease data from CSV
def load_disease_data():
    path = os.path.join(os.path.dirname(__file__), "..", "data", "genetic_diseases.csv")
    if not os.path.exists(path):
        return pd.DataFrame(columns=["Disease", "Genes", "Description", "Symptoms"])
    
    df = pd.read_csv(path)
    required_cols = {"Disease", "Genes", "Description", "Symptoms"}
    if not required_cols.issubset(df.columns):
        raise ValueError(f"CSV must contain columns: {required_cols}")
    return df

# Extract meaningful keywords from user input using NLP
def extract_keywords(text: str) -> str:
    doc = nlp(text)
    return " ".join([
        token.lemma_.lower() for token in doc
        if token.pos_ in ["NOUN", "ADJ", "VERB"] and not token.is_stop and token.is_alpha
    ])

# Translate text to desired language
def translate(text: str, lang: str = "en") -> str:
    return translator.translate(text, tgt_lang=lang)

# Main disease matching and response function
def match_disease(user_input: str, lang: str = "en", user_profile: dict = None) -> str:
    df = load_disease_data()
    if df.empty:
        return translate("⚠️ No disease data found. Please ensure 'data/genetic_diseases.csv' is present.", lang)

    input_processed = extract_keywords(user_input)
    if not input_processed.strip():
        return translate("❌ Could not extract meaningful symptoms. Please describe your condition in more detail.", lang)

    symptom_texts = df["Symptoms"].fillna("").apply(extract_keywords).tolist()
    tfidf = TfidfVectorizer()
    vectors = tfidf.fit_transform([input_processed] + symptom_texts)
    similarities = cosine_similarity(vectors[0:1], vectors[1:]).flatten()

    top_idx = similarities.argmax()
    best_score = similarities[top_idx]

    if best_score < 0.2:
        return translate("❌ Sorry, no strong matches found. Try listing more symptoms or rephrasing.", lang)

    match = df.iloc[top_idx]
    response = (
        f"🧬 **Disease Match:** {match['Disease']}\n"
        f"🧪 **Gene(s):** {match['Genes']}\n"
        f"📖 **Description:** {match['Description']}\n"
        f"🧠 **Common Symptoms:** {match['Symptoms']}\n"
        f"✅ **Confidence Score:** {round(best_score * 100, 1)}%"
    )

    if user_profile:
        profile_str = " | ".join([f"{k.capitalize()}: {v}" for k, v in user_profile.items()])
        response += f"\n\n👤 **Your Profile**: {profile_str}"

    response += "\n\n💡 Would you like treatment guidance, prevention tips, or SNP links for this disease?"
    return translate(response, lang)
