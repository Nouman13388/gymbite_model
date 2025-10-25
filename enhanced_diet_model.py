import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor


class EnhancedDietPredictor:
    def __init__(self):
        self.model = None
        self.feature_names = None
        self.target_names = ['Recommended_Calories', 'Recommended_Protein', 'Recommended_Carbs', 'Recommended_Fats']

    def calculate_bmr(self, age, weight, height, gender):
        """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
        if gender.lower() == 'male':
            return 10 * weight + 6.25 * height - 5 * age + 5
        elif gender.lower() == 'female':
            return 10 * weight + 6.25 * height - 5 * age - 161
        else:
            return 10 * weight + 6.25 * height - 5 * age - 78

    def calculate_tdee(self, bmr, exercise_frequency, daily_steps):
        """Calculate Total Daily Energy Expenditure"""
        if exercise_frequency >= 6:
            activity_multiplier = 1.725
        elif exercise_frequency >= 4:
            activity_multiplier = 1.55
        elif exercise_frequency >= 2:
            activity_multiplier = 1.375
        else:
            activity_multiplier = 1.2

        if daily_steps > 12000:
            activity_multiplier += 0.1
        elif daily_steps > 8000:
            activity_multiplier += 0.05

        return bmr * activity_multiplier

    def calculate_health_risk_score(self, bmi, blood_pressure_sys, blood_pressure_dia, cholesterol, blood_sugar, age):
        """Calculate health risk score (0-100, higher = more risk)"""
        risk_score = 0

        if bmi >= 30:
            risk_score += 25
        elif bmi >= 25:
            risk_score += 15
        elif bmi < 18.5:
            risk_score += 10

        if blood_pressure_sys >= 140 or blood_pressure_dia >= 90:
            risk_score += 20
        elif blood_pressure_sys >= 130 or blood_pressure_dia >= 80:
            risk_score += 10

        if cholesterol >= 240:
            risk_score += 15
        elif cholesterol >= 200:
            risk_score += 8

        if blood_sugar >= 126:
            risk_score += 20
        elif blood_sugar >= 100:
            risk_score += 10

        if age >= 65:
            risk_score += 10
        elif age >= 50:
            risk_score += 5

        return min(risk_score, 100)

    def validate_prediction(self, calories, protein, carbs, fats, bmr):
        """Apply health-safe bounds to predictions"""
        min_calories = bmr * 0.8
        max_calories = bmr * 2.0
        safe_calories = np.clip(calories, min_calories, max_calories)

        approx_weight = bmr / 15
        min_protein = approx_weight * 0.8
        max_protein = approx_weight * 2.5
        safe_protein = np.clip(protein, min_protein, max_protein)

        total_macro_calories = safe_protein * 4 + carbs * 4 + fats * 9

        if total_macro_calories > safe_calories * 1.1:
            scale_factor = safe_calories / total_macro_calories
            safe_protein *= scale_factor
            carbs *= scale_factor
            fats *= scale_factor

        return safe_calories, safe_protein, carbs, fats

    def predict(self, user_data):
        """Make prediction for a single user"""
        if self.model is None:
            raise ValueError("Model not trained yet!")

        user_df = pd.DataFrame([user_data])

        user_df['BMR'] = self.calculate_bmr(
            user_data['Age'], user_data['Weight_kg'],
            user_data['Height_cm'], user_data['Gender']
        )
        user_df['TDEE'] = self.calculate_tdee(
            user_df['BMR'].iloc[0], user_data['Exercise_Frequency'], user_data['Daily_Steps']
        )
        user_df['Health_Risk_Score'] = self.calculate_health_risk_score(
            user_data['BMI'], user_data['Blood_Pressure_Systolic'],
            user_data['Blood_Pressure_Diastolic'], user_data['Cholesterol_Level'],
            user_data['Blood_Sugar_Level'], user_data['Age']
        )
        user_df['Activity_Level_Score'] = (
            (user_data['Exercise_Frequency'] / 7) * 5 +
            (np.clip(user_data['Daily_Steps'] / 15000, 0, 1)) * 5
        )
        user_df['Sleep_Quality_Score'] = np.clip(user_data['Sleep_Hours'] / 8 * 10, 0, 10)

        user_features = user_df[self.feature_names]
        prediction = self.model.predict(user_features)[0]

        safe_prediction = self.validate_prediction(
            prediction[0], prediction[1], prediction[2], prediction[3], user_df['BMR'].iloc[0]
        )

        return {
            'recommended_calories': round(safe_prediction[0]),
            'recommended_protein': round(safe_prediction[1], 1),
            'recommended_carbs': round(safe_prediction[2], 1),
            'recommended_fats': round(safe_prediction[3], 1),
            'bmr': round(user_df['BMR'].iloc[0]),
            'tdee': round(user_df['TDEE'].iloc[0]),
            'health_risk_score': round(user_df['Health_Risk_Score'].iloc[0]),
            'activity_level_score': round(user_df['Activity_Level_Score'].iloc[0], 1)
        }

    def save_model(self, filename='enhanced_diet_predictor.pkl'):
        """Save the trained model"""
        joblib.dump((self.model, self.feature_names, self.target_names), filename)
        print(f"✅ Enhanced model saved as '{filename}'")

    def load_model(self, filename='enhanced_diet_predictor.pkl'):
        """Load a trained model"""
        self.model, self.feature_names, self.target_names = joblib.load(filename)
        print(f"✅ Enhanced model loaded from '{filename}'")
