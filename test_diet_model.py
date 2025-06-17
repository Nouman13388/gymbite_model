import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score
import joblib

# Load the dataset
df = pd.read_csv(r'C:\Users\Nouman\Downloads\Personalized_Diet_Recommendations.csv')
print("✅ Data Loaded")

# Drop duplicates if any
df.drop_duplicates(inplace=True)

# Select only numeric features
numeric_df = df.select_dtypes(include=[np.number])

# Check if target column exists
if 'Recommended_Calories' not in numeric_df.columns:
    print("Column 'Recommended_Calories' not found.")
    exit()

# Define input (X) and output (y)
X = numeric_df.drop('Recommended_Calories', axis=1)
y = numeric_df['Recommended_Calories']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = RandomForestRegressor(random_state=42)
model.fit(X_train, y_train)

# Predict and evaluate
y_pred = model.predict(X_test)
r2 = r2_score(y_test, y_pred)
print(f"R2 Score: {r2:.2f}")

# Save model for later use
joblib.dump((model, list(X.columns)), 'calorie_predictor.pkl')
print("Model saved as 'calorie_predictor.pkl'")

# Show feature importances
importances = model.feature_importances_
indices = np.argsort(importances)

plt.figure(figsize=(8, 6))
plt.barh(range(len(indices)), importances[indices], color='skyblue')
plt.yticks(range(len(indices)), [X.columns[i] for i in indices])
plt.title('Feature Importances')
plt.xlabel('Relative Importance')
plt.tight_layout()
plt.savefig("feature_importance.png")
print("Feature importance plot saved as 'feature_importance.png'")
