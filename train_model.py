# train_model.py

import joblib
import re
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import scipy.sparse as sp
import numpy as np

print("🚀 Starting model training process...")

# 1. Sample Data (a tiny dataset for demonstration)
# In a real project, you would use thousands of emails.
emails = [
    "URGENT! You have won a 1 week FREE membership in our $100,000 Prize scheme. T&C apply.",
    "WINNER!! As a valued network customer you have been selected to receive a £900 prize reward!",
    "Had your mobile 11 months or more? U R entitled to Update to the latest colour mobiles with camera for Free!",
    "Hi team, can we schedule a meeting for tomorrow at 10 AM? Please confirm.",
    "Please see attached the latest report. Let me know if you have any questions.",
    "Don't forget the party this Friday. It's going to be fun!",
    "Make money fast! Click here for a limited time offer on this amazing investment opportunity.",
    "Your account has been suspended. Click here to reactivate it immediately."
]
# Labels: 1 for spam, 0 for not spam (ham)
labels = [1, 1, 1, 0, 0, 0, 1, 1]

# 2. Define Spam Keywords
# These are used as an extra feature for the model.
spam_keywords = [
    'urgent', 'winner', 'prize', 'free', 'offer', 'limited time', 'click here',
    'money', 'investment', 'opportunity', 'claim', 'reward', 'congratulations'
]

# 3. Preprocessing Function
def preprocess_text(text):
    text = text.lower()
    text = re.sub(f"[{string.punctuation}]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

print("   - Preprocessing sample data...")
cleaned_emails = [preprocess_text(email) for email in emails]

# 4. Feature Engineering
# We will use TF-IDF for text features and add a custom keyword feature.
vectorizer = TfidfVectorizer(stop_words='english', max_features=100)
tfidf_features = vectorizer.fit_transform(cleaned_emails)

# Create the keyword feature (1 if a spam keyword is present, 0 otherwise)
keyword_features = np.array([[1 if any(word in email for word in spam_keywords) else 0] for email in cleaned_emails])

# Combine TF-IDF features with our custom keyword feature
final_features = sp.hstack([tfidf_features, keyword_features])

# 5. Model Training
print("   - Training Logistic Regression model...")
model = LogisticRegression()
model.fit(final_features, labels)

# 6. Save the Components
print("   - Saving model and components to .pkl files...")
try:
    joblib.dump(model, "spam_model.pkl")
    joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
    joblib.dump(spam_keywords, "spam_keywords.pkl")
    print("\n✅ Success! The following files have been created:")
    print("   - spam_model.pkl")
    print("   - tfidf_vectorizer.pkl")
    print("   - spam_keywords.pkl")
except Exception as e:
    print(f"\n❌ Error saving files: {e}")