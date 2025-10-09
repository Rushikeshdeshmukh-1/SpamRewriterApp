import joblib
from sklearn.feature_extraction.text import TfidfVectorizer

# Dummy spam model (always predicts 'ham')
class DummyModel:
    def predict(self, X):
        return ["ham"] * len(X)

# Save dummy model
joblib.dump(DummyModel(), "spam_model.pkl")

# Save dummy TF-IDF vectorizer
vectorizer = TfidfVectorizer()
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")

# Save dummy spam keywords list
spam_keywords = ["free", "offer", "win", "click", "money"]
joblib.dump(spam_keywords, "spam_keywords.pkl")

print("✅ Dummy model files created successfully!")
