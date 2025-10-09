import joblib
import re
import string
import scipy.sparse as sp

class SpamDetector:
    def __init__(self):
        # Load trained Logistic Regression model, vectorizer, and keywords
        self.model = joblib.load("spam_model.pkl")
        self.vectorizer = joblib.load("tfidf_vectorizer.pkl")
        self.spam_keywords = joblib.load("spam_keywords.pkl")

    def preprocess_text(self, text):
        text = text.lower()
        text = re.sub(f"[{string.punctuation}]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def predict_spam(self, text):
        cleaned_text = self.preprocess_text(text)
        tfidf_features = self.vectorizer.transform([cleaned_text])

        # Keyword flag feature
        keyword_flag = 1 if any(word in cleaned_text for word in self.spam_keywords) else 0
        final_features = sp.hstack([tfidf_features, [[keyword_flag]]])

        prediction = self.model.predict(final_features)[0]
        probability = self.model.predict_proba(final_features)[0][1]

        if keyword_flag:
            probability = min(probability + 0.1, 1.0)

        return {
            "is_spam": bool(prediction),
            "confidence": round(float(probability), 2),
            "method": "Logistic Regression + TF-IDF"
        }
