import pandas as pd
from sklearn.tree import DecisionTreeClassifier
import joblib

def train_model():
    # Simulated SNP-genotype dataset
    data = pd.DataFrame({
        "rs1234": ["AA", "AG", "GG", "AA", "AG", "GG"],
        "rs4567": ["TT", "CT", "CC", "CT", "TT", "CC"],
        "rs7890": ["CG", "CC", "GG", "CG", "CC", "GG"],
        "nutrition": ["High Folate", "Moderate Folate", "Low Folate", 
                      "Moderate Vitamin D", "High Vitamin D", "Normal"]
    })

    # Convert genotypes to numeric
    X = pd.get_dummies(data[["rs1234", "rs4567", "rs7890"]])
    y = data["nutrition"]

    clf = DecisionTreeClassifier()
    clf.fit(X, y)

    joblib.dump(clf, "nutrition/snp_model.pkl")
    print("✅ Model trained and saved!")

def predict_from_model(snp_df):
    clf = joblib.load("nutrition/snp_model.pkl")
    input_df = pd.get_dummies(snp_df)
    input_df = input_df.reindex(columns=clf.feature_names_in_, fill_value=0)
    return clf.predict(input_df)[0]
