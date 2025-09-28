# Teammate 2: ML Model Part
# This file loads the spam detection model and provides a prediction function.

from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch

# --- Configuration ---
# Define the model name from Hugging Face
MODEL_NAME = "prithivMLmods/Spam-Bert-Uncased" # Correct
print("Loading spam detection model... (This may take a moment on first run)")

# --- Model Loading ---
# Load the tokenizer and model once when the module is imported for efficiency.
try:
    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
    print("Spam detection model loaded successfully. ✅")
except Exception as e:
    print(f"Error loading model '{MODEL_NAME}': {e}")
    # Set to None to indicate failure
    tokenizer, model = None, None


# --- Core Function ---

# --- Core Function ---

def predict_spam(text: str, torch=None) -> str:
    """
    Predicts if a given text is 'Spam' or 'Not Spam'.
    This final version is robust and handles different model label schemes (e.g., "Spam", "spam", "LABEL_1").

    Args:
        text (str): The email text to classify.

    Returns:
        str: The prediction, either "Spam" or "Not Spam".
    """
    if not tokenizer or not model:
        return "Error: Model not loaded."

    # Tokenize the input text
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)

    # Perform inference
    with torch.no_grad():
        outputs = model(**inputs)
    """
    Spam Detection Module
    Author: [ML Teammate Name]
    Description: Handles spam detection using pre-trained BERT model from HuggingFace

    TODO for ML teammate:
    1. Install required packages: pip install transformers torch
    2. Choose a pre-trained model (suggested: "prithivMLmods/Spam-Bert-Uncased")
    3. Implement the prediction logic
    4. Test with sample emails
    """

    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch
    from typing import Dict, Any
    import logging

    class SpamDetector:
        """
        A class to detect spam emails using pre-trained BERT model
        """

        def __init__(self, model_name: str = "prithivMLmods/Spam-Bert-Uncased"):
            """
            Initialize the spam detector with a pre-trained model

            Args:
                model_name (str): HuggingFace model name for spam detection
            """
            self.model_name = model_name

            # Set up logging
            logging.basicConfig(level=logging.INFO)
            self.logger = logging.getLogger(__name__)

            # TODO: Initialize tokenizer and model
            self.tokenizer = None
            self.model = None

            # Load the model
            self.load_model()

        def load_model(self):
            """
            Load the pre-trained model and tokenizer
            """
            try:
                self.logger.info(f"Loading model: {self.model_name}")

                # TODO: Implement model loading
                # self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
                # self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)

                # For now, using placeholder
                self.logger.warning("Model loading not implemented yet - using dummy predictions")

            except Exception as e:
                self.logger.error(f"Error loading model: {str(e)}")

        def predict_spam(self, email_text: str) -> Dict[str, Any]:
            """
            Predict if an email is spam or not

            Args:
                email_text (str): The email text to analyze

            Returns:
                Dict: Contains 'is_spam', 'confidence', 'label'
            """

            # TODO: Implement actual prediction logic
            # Here's the structure your teammates should follow:

            try:
                # Input validation
                if not email_text or not email_text.strip():
                    return {
                        'is_spam': False,
                        'confidence': 0.0,
                        'label': 'ham',
                        'error': 'Empty email text'
                    }

                # TODO: Tokenize the input
                # inputs = self.tokenizer(email_text, return_tensors="pt", truncation=True, padding=True, max_length=512)

                # TODO: Get model prediction
                # with torch.no_grad():
                #     outputs = self.model(**inputs)
                #     predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
                #     predicted_class = torch.argmax(predictions, dim=-1).item()
                #     confidence = torch.max(predictions).item()

                # For demo purposes - replace with actual implementation
                # This is a dummy implementation based on simple keywords
                spam_keywords = ['urgent', 'money', 'click', 'limited time', '$$$', '!!!']
                email_lower = email_text.lower()
                spam_count = sum(1 for keyword in spam_keywords if keyword in email_lower)

                is_spam = spam_count >= 2  # Simple rule
                confidence = min(0.5 + (spam_count * 0.1), 0.95)  # Fake confidence
                label = 'spam' if is_spam else 'ham'

                return {
                    'is_spam': is_spam,
                    'confidence': confidence,
                    'label': label,
                    'error': None
                }

            except Exception as e:
                self.logger.error(f"Error during prediction: {str(e)}")
                return {
                    'is_spam': False,
                    'confidence': 0.0,
                    'label': 'ham',
                    'error': str(e)
                }

    # Example usage for ML teammate
    if __name__ == "__main__":
        # Test the spam detector
        detector = SpamDetector()

        # Test emails
        test_emails = [
            "URGENT!!! Make money fast!!! Click now!!!",
            "Hi John, let's meet for coffee tomorrow at 3 PM.",
            "Limited time offer! Get rich quick with this amazing opportunity!",
            "Your meeting has been scheduled for next week."
        ]

        for email in test_emails:
            result = detector.predict_spam(email)
            print(f"Email: {email[:50]}...")
            print(f"Prediction: {result['label']} (confidence: {result['confidence']:.2f})")
            print("-" * 60)

    """
    IMPLEMENTATION GUIDE FOR ML TEAMMATE:

    1. Install dependencies:
       pip install transformers torch

    2. Research and choose a model:
       - "prithivMLmods/Spam-Bert-Uncased" (suggested)
       - Or any other spam detection model from HuggingFace

    3. Key functions to implement:
       - load_model(): Load tokenizer and model
       - predict_spam(): Main prediction function

    4. Model usage pattern:
       ```python
       # Tokenize
       inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)

       # Predict
       with torch.no_grad():
           outputs = model(**inputs)
           predictions = F.softmax(outputs.logits, dim=-1)
       ```

    5. Return format should match the existing structure for GUI integration

    6. Test with various email samples to ensure accuracy

    7. Handle edge cases (empty text, very long emails, etc.)
    """