import joblib
import pandas as pd

# Load model and feature names
model, feature_names = joblib.load('calorie_predictor.pkl')

# Provide input matching the training feature set
sample_input = pd.DataFrame([{
    'Age': 28,
    'BMI': 23.5,
    'Heart_Rate': 72,
    'Steps_Per_Day': 7000,
    'Blood_Pressure_Systolic': 120,
    'Blood_Pressure_Diastolic': 80,
    'Sleep_Hours': 7.5,
    'Caloric_Intake': 2000,
    'Protein_Intake': 75,
    'Carbohydrate_Intake': 250,
    'Fat_Intake': 60,
    'Cholesterol': 180,
    'Blood_Sugar_Level': 95
}], columns=feature_names)

# Make prediction
predicted_calories = model.predict(sample_input)[0]
print(f"Predicted Recommended Calories: {round(predicted_calories)} kcal")
