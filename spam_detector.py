"""
Spam Detection Module - FIXED VERSION
Author: ML Teammate (Completed)
Description: Handles spam detection using rule-based approach with BERT fallback
"""

import logging
from typing import Dict, Any

# Optional BERT imports - will use rule-based if not available
try:
    from transformers import AutoTokenizer, AutoModelForSequenceClassification
    import torch
    TRANSFORMERS_AVAILABLE = True
except ImportError:
    TRANSFORMERS_AVAILABLE = False

class SpamDetector:
    """
    A class to detect spam emails using rule-based detection with optional BERT enhancement
    """

    def __init__(self, model_name: str = "unitary/toxic-bert"):
        """
        Initialize the spam detector

        Args:
            model_name (str): HuggingFace model name (optional)
        """
        self.model_name = model_name

        # Set up logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        # Initialize models
        self.tokenizer = None
        self.model = None
        self.use_bert = False

        # Try to load BERT model
        if TRANSFORMERS_AVAILABLE:
            self.load_bert_model()
        else:
            self.logger.info("Transformers not available, using rule-based detection only")

    def load_bert_model(self):
        """
        Try to load the BERT model (optional enhancement)
        """
        try:
            self.logger.info(f"Attempting to load BERT model: {self.model_name}")
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            self.model = AutoModelForSequenceClassification.from_pretrained(self.model_name)
            self.model.eval()
            self.use_bert = True
            self.logger.info("BERT model loaded successfully")

        except Exception as e:
            self.logger.warning(f"Failed to load BERT model: {str(e)}")
            self.logger.info("Falling back to rule-based detection")
            self.use_bert = False

    def rule_based_prediction(self, email_text: str) -> Dict[str, Any]:
        """
        Rule-based spam detection - main detection method
        """
        # Convert to lowercase for analysis
        email_lower = email_text.lower()
        email_upper = email_text.upper()

        # Spam indicators
        spam_keywords = [
            'urgent', 'money', 'click', 'limited time', 'winner', 'congratulations',
            'free', 'offer', 'deal', 'guaranteed', 'risk free', 'act now', 'call now',
            'credit card', 'cash', 'earn money', 'make money', 'work from home',
            'lose weight', 'casino', 'lottery', 'prize', 'claim now', 'limited offer',
            'discount', 'save money', 'financial freedom', 'get rich', 'opportunity',
            'investment', 'profit', 'income', 'bonus', 'reward'
        ]

        spam_patterns = [
            'URGENT!!!', 'FREE!!!', 'WINNER!!!', '100% FREE', 'LIMITED TIME!!!',
            'ACT NOW!!!', 'CALL NOW!!!', 'CLICK HERE!!!', 'GUARANTEED!!!',
            'RISK FREE!!!', 'MONEY BACK!!!', 'NO RISK!!!'
        ]

        # Analysis metrics
        keyword_matches = sum(1 for keyword in spam_keywords if keyword in email_lower)
        pattern_matches = sum(1 for pattern in spam_patterns if pattern in email_upper)

        # Punctuation analysis
        exclamation_groups = email_text.count('!!!')
        dollar_symbols = email_text.count('$')
        caps_ratio = sum(1 for c in email_text if c.isupper()) / len(email_text) if email_text else 0

        # Calculate spam score
        spam_score = (
            keyword_matches * 0.1 +           # Keyword weight
            pattern_matches * 0.2 +           # Pattern weight
            exclamation_groups * 0.15 +       # Excessive punctuation
            min(dollar_symbols * 0.1, 0.3) +  # Money symbols (capped)
            caps_ratio * 0.25                 # Excessive caps
        )

        # Additional context checks
        if any(phrase in email_lower for phrase in ['click here', 'act now', 'limited time']):
            spam_score += 0.2

        if any(phrase in email_lower for phrase in ['make money fast', 'get rich quick']):
            spam_score += 0.3

        # Determine classification
        is_spam = spam_score > 0.4
        confidence = min(max(spam_score * 2, 0.1), 0.95)  # Scale to 0.1-0.95 range

        return {
            'is_spam': is_spam,
            'confidence': confidence,
            'label': 'spam' if is_spam else 'ham',
            'error': None,
            'method': 'rule-based',
            'spam_score': spam_score,
            'indicators': {
                'keywords': keyword_matches,
                'patterns': pattern_matches,
                'exclamations': exclamation_groups,
                'caps_ratio': caps_ratio
            }
        }

    def bert_prediction(self, email_text: str) -> Dict[str, Any]:
        """
        BERT-based prediction (enhancement when available)
        """
        if not self.use_bert or not self.tokenizer or not self.model:
            return self.rule_based_prediction(email_text)

        try:
            # Tokenize input
            inputs = self.tokenizer(
                email_text,
                return_tensors="pt",
                truncation=True,
                padding=True,
                max_length=512
            )

            # Get prediction
            with torch.no_grad():
                outputs = self.model(**inputs)
                predictions = torch.nn.functional.softmax(outputs.logits, dim=-1)
                predicted_class = torch.argmax(predictions, dim=-1).item()
                confidence = torch.max(predictions).item()

            # Interpret results (for toxic-bert: 1 = toxic/spam, 0 = clean/ham)
            is_spam = predicted_class == 1
            label = 'spam' if is_spam else 'ham'

            # Combine with rule-based for better accuracy
            rule_result = self.rule_based_prediction(email_text)

            # If either method detects spam with high confidence, classify as spam
            if (is_spam and confidence > 0.7) or (rule_result['is_spam'] and rule_result['confidence'] > 0.7):
                final_is_spam = True
                final_confidence = max(confidence, rule_result['confidence'])
            else:
                final_is_spam = False
                final_confidence = min(confidence, rule_result['confidence'])

            return {
                'is_spam': final_is_spam,
                'confidence': final_confidence,
                'label': 'spam' if final_is_spam else 'ham',
                'error': None,
                'method': 'bert+rules',
                'bert_prediction': predicted_class,
                'rule_score': rule_result['spam_score']
            }

        except Exception as e:
            self.logger.error(f"BERT prediction failed: {str(e)}")
            return self.rule_based_prediction(email_text)

    def predict_spam(self, email_text: str) -> Dict[str, Any]:
        """
        Main prediction method

        Args:
            email_text (str): The email text to analyze

        Returns:
            Dict: Contains prediction results
        """
        try:
            # Input validation
            if not email_text or not email_text.strip():
                return {
                    'is_spam': False,
                    'confidence': 0.0,
                    'label': 'ham',
                    'error': 'Empty email text',
                    'method': 'validation'
                }

            # Use BERT if available, otherwise rule-based
            if self.use_bert:
                return self.bert_prediction(email_text)
            else:
                return self.rule_based_prediction(email_text)

        except Exception as e:
            self.logger.error(f"Prediction error: {str(e)}")
            return {
                'is_spam': False,
                'confidence': 0.0,
                'label': 'ham',
                'error': str(e),
                'method': 'error'
            }

# Test the detector
if __name__ == "__main__":
    print("🔍 Testing Spam Detection System")
    print("=" * 50)

    detector = SpamDetector()

    test_emails = [
        "URGENT!!! Make money fast!!! Click now!!! Limited time offer!!!",
        "Hi John, let's meet for coffee tomorrow at 3 PM. Looking forward to it.",
        "LIMITED TIME OFFER! Get rich quick with this amazing opportunity! 100% FREE!!! ACT NOW!!!",
        "Your meeting has been scheduled for next week. Please confirm your attendance.",
        "CONGRATULATIONS!!! You are a WINNER!!! Claim your $$$$ prize now!!! Risk FREE!!!",
        "Please review the attached document and let me know if you have any questions.",
        "URGENT BUSINESS PROPOSAL!!! Contact me IMMEDIATELY for $15,000,000 opportunity!!!"
    ]

    for i, email in enumerate(test_emails, 1):
        print(f"\n📧 Test {i}:")
        print(f"Email: {email[:60]}{'...' if len(email) > 60 else ''}")

        result = detector.predict_spam(email)

        status = "🚨 SPAM" if result['is_spam'] else "✅ HAM"
        print(f"Result: {status}")
        print(f"Confidence: {result['confidence']:.1%}")
        print(f"Method: {result['method']}")

        if 'indicators' in result:
            indicators = result['indicators']
            print(f"Indicators: Keywords({indicators['keywords']}), Patterns({indicators['patterns']}), Caps({indicators['caps_ratio']:.2f})")

        print("-" * 50)