# ---------------- Step 0: Setup ----------------
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
import scipy.sparse as sp
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import joblib

# ---------------- Step 1: Load CSV ----------------
df = pd.read_csv("spam.csv",encoding="latin1")  # CSV with columns 'label' and 'text'
df = df[['v1', 'v2']]
df.columns = ['label', 'text']

# Convert label: spam=1, ham=0
df['label'] = df['label'].map({'spam':1, 'ham':0})

# ---------------- Step 2: Add Spam Keywords Feature ----------------
spam_keywords = ["win", "free", "congratulations", "click", "urgent", "cash", "offer", "buy now"]

def keyword_flag(text):
    text = str(text).lower()
    for word in spam_keywords:
        if word in text:
            return 1
    return 0

df['keyword_flag'] = df['text'].apply(keyword_flag)

# ---------------- Step 3: TF-IDF Vectorization + Combine ----------------
vectorizer = TfidfVectorizer(max_features=3000)
X_text = vectorizer.fit_transform(df['text'])
X = sp.hstack([X_text, df['keyword_flag'].values.reshape(-1,1)])
y = df['label']

# ---------------- Step 4: Train/Test Split & Logistic Regression ----------------
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)

# ---------------- Step 5: Evaluate ----------------
y_pred = model.predict(X_test)
print("---- Classification Report ----")
print(classification_report(y_test, y_pred))
print("---- Confusion Matrix ----")
print(confusion_matrix(y_test, y_pred))

# ---------------- Step 6: Save Model, Vectorizer & Keywords ----------------
joblib.dump(model, "spam_classifier.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
joblib.dump(spam_keywords, "spam_keywords.pkl")

print("✅ Model, vectorizer, and keywords saved successfully!")

# ---------------- Step 7: Load Model, Vectorizer & Keywords ----------------
model = joblib.load("spam_classifier.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")
spam_keywords = joblib.load("spam_keywords.pkl")

