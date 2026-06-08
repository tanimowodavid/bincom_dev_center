import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report


script_dir = os.path.dirname(os.path.abspath(__file__))

def spam_classification():
    print("\n--- TASK 2: SPAM EMAIL CLASSIFICATION ---")
    
    # Load the dataset
    df = pd.read_csv(os.path.join(script_dir, 'spam_ham_dataset.csv'))
    
    # Data Cleaning & Preprocessing
    X_text = df['text']
    y_labels = df['label'].map({'ham': 0, 'spam': 1}) # Map text labels to 0 and 1
    
    # Train/Test Split
    X_train_text, X_test_text, y_train, y_test = train_test_split(X_text, y_labels, test_size=0.2, random_state=42)
    
    # Vectorization: Transform raw text strings into numerical word-count matrices
    vectorizer = CountVectorizer()
    X_train_vectorized = vectorizer.fit_transform(X_train_text)
    X_test_vectorized = vectorizer.transform(X_test_text)
    
    # Initialize and Train the Model
    # Multinomial Naive Bayes is the industry-standard baseline for text classification so... let's use it!
    model = MultinomialNB()
    model.fit(X_train_vectorized, y_train)
    print("Spam classifier training complete.")
    
    # Predictions & Evaluation
    y_pred = model.predict(X_test_vectorized)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nSpam Model Accuracy: {accuracy * 100:.2f}%")
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    spam_classification()