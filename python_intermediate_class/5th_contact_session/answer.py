import os
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler  # Transformer (Scales data)
from sklearn.ensemble import RandomForestRegressor  # Estimator (The Model)
from sklearn.pipeline import Pipeline  # The Assembly Line Container
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.datasets import fetch_california_housing
import joblib

def california_housing_pipeline():
    print("--- DAY 5: CALIFORNIA HOUSING WITH ML PIPELINES ---")
    
    X, y = fetch_california_housing(as_frame=True, return_X_y=True)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # 1. Define the Pipeline Assembly Line Steps
    # Format: ('name_of_step', ObjectInstance())
    housing_pipeline = Pipeline([
        ('scaler', StandardScaler()),                 # Step 1: Scale the numerical features
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42)) # Step 2: Run the model
    ])
    
    # 2. Train the entire pipeline in ONE command!
    # This automatically runs the scaler on X_train, transforms it, and feeds it to the forest model.
    print("Training the unified pipeline...")
    housing_pipeline.fit(X_train, y_train)
    print("Pipeline training complete.")
    
    # 3. Make predictions directly from raw test data
    # The pipeline automatically applies the scaler transformations to X_test before guessing!
    y_pred = housing_pipeline.predict(X_test)
    
    # Evaluation
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)
    print(f"\n[Pipeline] Mean Squared Error (MSE): {mse:.4f}")
    print(f"[Pipeline] R-squared (R²) Score: {r2:.4f}")
    
    # 4. Save the ENTIRE pipeline (scaler + model combined) into a single file!
    script_dir = os.path.dirname(os.path.abspath(__file__))
    pipeline_path = os.path.join(script_dir, 'california_housing_pipeline.pkl')
    joblib.dump(housing_pipeline, pipeline_path)
    print(f"\nEntire processing pipeline successfully saved to: {pipeline_path}")

if __name__ == "__main__":
    california_housing_pipeline()