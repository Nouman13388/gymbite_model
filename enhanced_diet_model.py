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

    def adjust_for_fitness_goal(self, tdee, goal, timeline):
        """Adjust calories based on fitness goal and timeline"""
        adjustments = {
            'weight_loss': {'aggressive': -750, 'moderate': -500, 'conservative': -300},
            'muscle_gain': {'aggressive': 600, 'moderate': 400, 'conservative': 250},
            'cutting': {'aggressive': -600, 'moderate': -400, 'conservative': -250},
            'bulking': {'aggressive': 600, 'moderate': 450, 'conservative': 300},
            'athletic': {'aggressive': 200, 'moderate': 100, 'conservative': 50},
            'maintenance': {'aggressive': 0, 'moderate': 0, 'conservative': 0}
        }
        
        adjustment = adjustments.get(goal, {}).get(timeline, 0)
        return tdee + adjustment

    def calculate_macro_ratios(self, goal, dietary_preference):
        """Calculate protein/carb/fat ratios based on goal and diet"""
        # Base ratios (protein%, carb%, fat%)
        goal_ratios = {
            'weight_loss': (0.35, 0.35, 0.30),
            'muscle_gain': (0.30, 0.45, 0.25),
            'cutting': (0.40, 0.30, 0.30),
            'bulking': (0.25, 0.50, 0.25),
            'athletic': (0.30, 0.45, 0.25),
            'maintenance': (0.25, 0.45, 0.30)
        }
        
        # Adjust for dietary preferences
        protein_pct, carb_pct, fat_pct = goal_ratios.get(goal, (0.25, 0.45, 0.30))
        
        if dietary_preference == 'vegan' or dietary_preference == 'vegetarian':
            protein_pct = max(0.20, protein_pct - 0.05)  # Slightly lower protein
            carb_pct += 0.05
        elif dietary_preference == 'keto':
            fat_pct = 0.70
            protein_pct = 0.25
            carb_pct = 0.05
            
        return protein_pct, carb_pct, fat_pct

    def calculate_meal_distribution(self, total_calories, protein_g, carbs_g, fats_g, meal_frequency, timing_preference):
        """Distribute macros across meals based on frequency and timing"""
        meals = []
        
        # Define meal distribution patterns
        if meal_frequency == 2:
            meal_names = ['Breakfast', 'Dinner']
            if timing_preference == 'front_loaded':
                percentages = [0.60, 0.40]
            elif timing_preference == 'back_loaded':
                percentages = [0.40, 0.60]
            else:  # balanced
                percentages = [0.50, 0.50]
        elif meal_frequency == 3:
            meal_names = ['Breakfast', 'Lunch', 'Dinner']
            if timing_preference == 'front_loaded':
                percentages = [0.40, 0.35, 0.25]
            elif timing_preference == 'back_loaded':
                percentages = [0.25, 0.35, 0.40]
            else:  # balanced
                percentages = [0.33, 0.34, 0.33]
        elif meal_frequency == 4:
            meal_names = ['Breakfast', 'Lunch', 'Snack', 'Dinner']
            if timing_preference == 'front_loaded':
                percentages = [0.35, 0.30, 0.15, 0.20]
            elif timing_preference == 'back_loaded':
                percentages = [0.20, 0.25, 0.15, 0.40]
            else:  # balanced
                percentages = [0.28, 0.28, 0.14, 0.30]
        elif meal_frequency == 5:
            meal_names = ['Breakfast', 'Mid-Morning Snack', 'Lunch', 'Afternoon Snack', 'Dinner']
            if timing_preference == 'front_loaded':
                percentages = [0.30, 0.15, 0.25, 0.10, 0.20]
            elif timing_preference == 'back_loaded':
                percentages = [0.20, 0.10, 0.20, 0.15, 0.35]
            else:  # balanced
                percentages = [0.25, 0.12, 0.26, 0.12, 0.25]
        else:  # 6 meals
            meal_names = ['Breakfast', 'Mid-Morning', 'Lunch', 'Afternoon', 'Dinner', 'Evening']
            percentages = [0.20, 0.15, 0.20, 0.15, 0.20, 0.10]  # balanced default
        
        for i, meal_name in enumerate(meal_names):
            pct = percentages[i]
            meals.append({
                'meal': meal_name,
                'calories': round(total_calories * pct),
                'protein': round(protein_g * pct, 1),
                'carbs': round(carbs_g * pct, 1),
                'fats': round(fats_g * pct, 1)
            })
        
        return meals

    def build_dietary_constraints(self, user_data):
        """Package user preferences for meal generation"""
        return {
            'region': user_data.get('Region', 'Global'),
            'city': user_data.get('City'),
            'dietary_preference': user_data.get('Dietary_Preference', 'omnivore'),
            'excluded_ingredients': user_data.get('Excluded_Ingredients', []),
            'allergens': user_data.get('Allergens', []),
            'budget_level': user_data.get('Budget_Level', 'medium'),
            'cooking_time': user_data.get('Cooking_Time', 'moderate'),
            'cuisine_preference': user_data.get('Cuisine_Preference', 'local'),
            'meal_timing_preference': user_data.get('Meal_Timing_Preference', 'balanced')
        }

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
        """Make prediction for a single user with enhanced personalization"""
        if self.model is None:
            raise ValueError("Model not trained yet!")

        user_df = pd.DataFrame([user_data])

        # Calculate base metrics
        bmr = self.calculate_bmr(
            user_data['Age'], user_data['Weight_kg'],
            user_data['Height_cm'], user_data['Gender']
        )
        user_df['BMR'] = bmr
        
        tdee = self.calculate_tdee(
            bmr, user_data['Exercise_Frequency'], user_data['Daily_Steps']
        )
        user_df['TDEE'] = tdee
        
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

        # Get user preferences
        fitness_goal = user_data.get('Fitness_Goal', 'maintenance')
        goal_timeline = user_data.get('Goal_Timeline', 'moderate')
        dietary_preference = user_data.get('Dietary_Preference', 'omnivore')
        meal_frequency = user_data.get('Meal_Frequency', 3)
        timing_preference = user_data.get('Meal_Timing_Preference', 'balanced')

        # Adjust calories for fitness goal
        adjusted_calories = self.adjust_for_fitness_goal(tdee, fitness_goal, goal_timeline)
        
        # Calculate macro ratios based on goal and diet
        protein_pct, carb_pct, fat_pct = self.calculate_macro_ratios(fitness_goal, dietary_preference)
        
        # Calculate macros in grams
        protein_g = (adjusted_calories * protein_pct) / 4  # 4 cal/g
        carbs_g = (adjusted_calories * carb_pct) / 4  # 4 cal/g
        fats_g = (adjusted_calories * fat_pct) / 9  # 9 cal/g
        
        # Apply safety validation
        safe_calories, safe_protein, safe_carbs, safe_fats = self.validate_prediction(
            adjusted_calories, protein_g, carbs_g, fats_g, bmr
        )
        
        # Calculate meal distribution
        meal_distribution = self.calculate_meal_distribution(
            safe_calories, safe_protein, safe_carbs, safe_fats,
            meal_frequency, timing_preference
        )
        
        # Build dietary constraints for meal generation
        dietary_constraints = self.build_dietary_constraints(user_data)

        return {
            'nutritional_targets': {
                'recommended_calories': round(safe_calories),
                'recommended_protein': round(safe_protein, 1),
                'recommended_carbs': round(safe_carbs, 1),
                'recommended_fats': round(safe_fats, 1),
                'bmr': round(bmr),
                'tdee': round(tdee),
                'adjusted_for_goal': round(adjusted_calories),
                'macro_split': {
                    'protein_percent': round(protein_pct * 100),
                    'carbs_percent': round(carb_pct * 100),
                    'fats_percent': round(fat_pct * 100)
                }
            },
            'meal_distribution': meal_distribution,
            'dietary_constraints': dietary_constraints,
            'health_metrics': {
                'health_risk_score': round(user_df['Health_Risk_Score'].iloc[0]),
                'activity_level_score': round(user_df['Activity_Level_Score'].iloc[0], 1),
                'sleep_quality_score': round(user_df['Sleep_Quality_Score'].iloc[0], 1)
            },
            'personalization': {
                'fitness_goal': fitness_goal,
                'goal_timeline': goal_timeline,
                'dietary_preference': dietary_preference,
                'meal_frequency': meal_frequency
            }
        }

    def save_model(self, filename='enhanced_diet_predictor.pkl'):
        """Save the trained model"""
        joblib.dump((self.model, self.feature_names, self.target_names), filename)
        print(f"✅ Enhanced model saved as '{filename}'")

    def load_model(self, filename='enhanced_diet_predictor.pkl'):
        """Load a trained model"""
        self.model, self.feature_names, self.target_names = joblib.load(filename)
        print(f"✅ Enhanced model loaded from '{filename}'")
