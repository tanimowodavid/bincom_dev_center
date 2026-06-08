import os
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report


script_dir = os.path.dirname(os.path.abspath(__file__))

def titanic_classification():
    print("--- TASK 1: TITANIC SURVIVAL PREDICTION ---")
    
    # Load the dataset
    df = pd.read_csv(os.path.join(script_dir, 'Titanic.csv'))
    
    # Standardize column names to lowercase just in case of any hidden spaces
    df.columns = df.columns.str.lower()
    print("Data loaded successfully. Columns found:", list(df.columns))
    
    # Data Cleaning & Preprocessing
    # Fill missing ages with the median age
    df['age'] = df['age'].fillna(df['age'].median())
    
    # Fill missing embarked values with the most common port 'S'
    df['embarked'] = df['embarked'].fillna('S')
    
    # Convert Categorical 'sex' to numeric (male = 0, female = 1)
    df['sex'] = df['sex'].map({'male': 0, 'female': 1})
    
    # Convert 'alone' boolean (True/False) to numeric (1/0)
    if 'alone' in df.columns:
        df['alone'] = df['alone'].astype(int)
    
    # One-Hot Encode both 'embarked' and 'class' text columns
    # drop_first=True prevents the dummy variable trap
    df = pd.get_dummies(df, columns=['embarked', 'class'], drop_first=True)
    
    # Dynamic Feature Selection based on your exact columns
    # After dummy encoding, 'class' (First, Second, Third) becomes class_Second and class_Third
    # 'embarked' (C, Q, S) becomes embarked_Q and embarked_S
    features = ['sex', 'age', 'sibsp', 'parch', 'fare', 'alone', 
                'embarked_q', 'embarked_s', 'class_second', 'class_third']
    
    # Convert feature names to lowercase to perfectly match get_dummies output
    df.columns = df.columns.str.lower()
    
    X = df[features]       # Predictors
    y = df['survived']     # Target variable
    
    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Initialize and Train the Model
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    print("Model training complete.")
    
    # Predictions & Evaluation
    y_pred = model.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"\nModel Accuracy: {accuracy * 100:.2f}%")
    model_path = os.path.join(script_dir, 'titanic_model.pkl')
    joblib.dump(model, model_path)
    print(f"\nModel successfully serialized and saved to: {model_path}")
    print("\nDetailed Classification Report:")
    print(classification_report(y_test, y_pred))

if __name__ == "__main__":
    titanic_classification()