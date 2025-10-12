import joblib
import re
import string
import logging
import scipy.sparse as sp

class SpamDetector:

    def __init__(self):
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        try:
            self.model = joblib.load("spam_model.pkl")
            self.vectorizer = joblib.load("tfidf_vectorizer.pkl")
            self.spam_keywords = joblib.load("spam_keywords.pkl")
            self.logger.info("SpamDetector initialized successfully from .pkl files.")
        except FileNotFoundError as e:
            self.logger.error(f"Error loading model files: {e}. Make sure spam_model.pkl, tfidf_vectorizer.pkl, and spam_keywords.pkl are in the same directory.")
            self.model = None
            self.vectorizer = None
            self.spam_keywords = None
        except Exception as e:
            self.logger.error(f"An unexpected error occurred during initialization: {e}")
            self.model = None
            self.vectorizer = None
            self.spam_keywords = None

    def _preprocess_text(self, text: str) -> str:
        text = text.lower()
        text = re.sub(f"[{string.punctuation}]", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return text

    def predict_spam(self, email_text: str) -> dict:
        if not email_text or not email_text.strip():
            return {
                'is_spam': False, 'confidence': 0.0, 'label': 'ham',
                'error': 'Email text cannot be empty', 'method': 'validation'
            }

        if not all([self.model, self.vectorizer, self.spam_keywords]):
            return {
                'is_spam': False, 'confidence': 0.0, 'label': 'ham',
                'error': 'Detector not initialized. Missing model files.', 'method': 'error'
            }
        
        try:
            cleaned_text = self._preprocess_text(email_text)
            tfidf_features = self.vectorizer.transform([cleaned_text])
            keyword_flag = 1 if any(word in cleaned_text for word in self.spam_keywords) else 0
            final_features = sp.hstack([tfidf_features, [[keyword_flag]]])
            prediction = self.model.predict(final_features)[0]
            probability = self.model.predict_proba(final_features)[0][1]
            if keyword_flag and prediction == 1:
                probability = min(probability + 0.1, 1.0)

            is_spam = bool(prediction)
            
            return {
                'is_spam': is_spam,
                'confidence': float(probability),
                'label': 'spam' if is_spam else 'ham',
                'error': None,
                'method': 'Logistic Regression + TF-IDF'
            }
        
        except Exception as e:
            self.logger.error(f"Prediction failed: {e}")
            return {
                'is_spam': False, 'confidence': 0.0, 'label': 'ham',
                'error': str(e), 'method': 'error'
            }

if __name__ == "__main__":
    try:
        detector = SpamDetector()
        if detector.model: # Check if initialization was successful
            test_email = "URGENT!!! You have won a 1,000,000 dollar prize. CLICK HERE to claim."
            print(f"Testing email: '{test_email}'")
            result = detector.predict_spam(test_email)
            print("Prediction Result:")
            print(result)
        else:
            print("Could not run test because model files are missing.")
    except Exception as e:
        print(f"An error occurred during the test run: {e}")
