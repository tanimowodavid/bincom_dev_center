import os
import joblib
import pandas as pd
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.metrics import accuracy_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

def titanic_pipeline_task():
    print("--- TITANIC CLASSIFICATION WITH ML PIPELINES ---")
    
    # Load raw data
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'datasets/Titanic.csv')
    df = pd.read_csv(csv_path)
    
    # Standardize column naming format
    df.columns = df.columns.str.lower()
    
    # Separate clues (X) and answers (y)
    # We will pick a mix of raw numerical columns and uncleaned text columns!
    features = ['age', 'fare', 'sex', 'class']
    X = df[features]
    y = df['survived']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Define cleaning steps for numerical columns (Age, Fare)
    # If an age is missing, automatically fill it with the median value
    numeric_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='median'))
    ])
    
    # Define cleaning steps for text/categorical columns (Sex, Class)
    # Automatically convert text labels into numbers using One-Hot Encoding
    categorical_transformer = Pipeline(steps=[
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])
    
    # Combine both cleaning stations into a master preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numeric_transformer, ['age', 'fare']),
            ('cat', categorical_transformer, ['sex', 'class'])
        ])
    
    # Pack the preprocessor and the machine learning model into the final Pipeline
    titanic_pipeline = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('classifier', LogisticRegression(max_iter=1000))
    ])
    
    # Fit the entire pipeline on completely RAW training data!
    print("Training the Titanic pipeline...")
    titanic_pipeline.fit(X_train, y_train)
    
    # Evaluate using the raw test data
    y_pred = titanic_pipeline.predict(X_test)
    print(f"Pipeline Test Accuracy: {accuracy_score(y_test, y_pred) * 100:.2f}%")
    
    # Save the pipeline file
    pipeline_path = os.path.join(script_dir, 'titanic_pipeline.pkl')
    joblib.dump(titanic_pipeline, pipeline_path)
    print(f"Saved complete Titanic pipeline to: {pipeline_path}")

if __name__ == "__main__":
    titanic_pipeline_task()