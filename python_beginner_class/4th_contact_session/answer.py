import pandas as pd
from sklearn.linear_model import LinearRegression

# =========================
# LOAD CSV
# =========================
df = pd.read_csv("4th_contact_session/student_scores.csv")

# Display dataset
print("Dataset:")
print(df)

# =========================
# PREPARE DATA
# =========================
# Independent variable (Hours)
X = df[["Hours"]]

# Dependent variable (Scores)
y = df["Scores"]

# =========================
# TRAIN MODEL
# =========================
model = LinearRegression()
model.fit(X, y)

# =========================
# RESULTS
# =========================
slope = model.coef_[0]
intercept = model.intercept_

print(f"\nSlope (m): {slope}")
print(f"Intercept (b): {intercept}")

# =========================
# PREDICTION
# =========================
hours = [[6]]
predicted_score = model.predict(hours)

print(f"\nPredicted score for {hours} hours: {predicted_score[0]}")
