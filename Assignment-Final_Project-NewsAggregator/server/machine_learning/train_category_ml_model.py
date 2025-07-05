import csv
import os
import joblib
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB


def load_keyword_data(path="docs/category_keywords.csv"):
    texts, labels = [], []
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            texts.append(row["keyword"].lower())
            labels.append(row["category"])
    return texts, labels


def train_and_save_model():
    X, y = load_keyword_data()

    vectorizer = CountVectorizer()
    X_vect = vectorizer.fit_transform(X)

    model = MultinomialNB()
    model.fit(X_vect, y)

    os.makedirs("docs", exist_ok=True)
    joblib.dump((model, vectorizer), "docs/trained_category_model.joblib")
    print("Model trained and saved.")


if __name__ == "__main__":
    train_and_save_model()
