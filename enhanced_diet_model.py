import warnings
warnings.filterwarnings('ignore')

import numpy as np
import pandas as pd
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor


class EnhancedDietPredictor:
    def __init__(self, config=None):
        self.model = None
        self.feature_names = None
        self.target_names = ['Recommended_Calories', 'Recommended_Protein', 'Recommended_Carbs', 'Recommended_Fats']
        self.config = config  # Will be set when loading model

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
        if not self.config:
            raise ValueError("Configuration not loaded. Please call load_model() first.")
        
        multipliers = self.config['nutrition']['activity_multipliers']
        
        # Determine activity level based on exercise frequency
        if exercise_frequency >= multipliers['very_active']['min_exercise_days']:
            activity_multiplier = multipliers['very_active']['multiplier']
        elif exercise_frequency >= multipliers['moderately_active']['min_exercise_days']:
            activity_multiplier = multipliers['moderately_active']['multiplier']
        elif exercise_frequency >= multipliers['lightly_active']['min_exercise_days']:
            activity_multiplier = multipliers['lightly_active']['multiplier']
        else:
            activity_multiplier = multipliers['sedentary']['multiplier']

        # Add step bonus
        step_bonus = self.config['nutrition']['step_bonus']
        if daily_steps > step_bonus['high_steps']['threshold']:
            activity_multiplier += step_bonus['high_steps']['bonus']
        elif daily_steps > step_bonus['medium_steps']['threshold']:
            activity_multiplier += step_bonus['medium_steps']['bonus']

        return bmr * activity_multiplier

    def calculate_health_risk_score(self, bmi, blood_pressure_sys, blood_pressure_dia, cholesterol, blood_sugar, age):
        """Calculate health risk score (0-100, higher = more risk)
        Note: Simplified calculation. For medical purposes, consult healthcare professionals."""
        # User can customize thresholds via API parameters if needed
        # This is a basic implementation using common health guidelines
        risk_score = 0

        # BMI assessment (WHO standards)
        if bmi >= 30:
            risk_score += 25
        elif bmi >= 25:
            risk_score += 15
        elif bmi < 18.5:
            risk_score += 10

        # Blood pressure (AHA guidelines)
        if blood_pressure_sys >= 140 or blood_pressure_dia >= 90:
            risk_score += 20
        elif blood_pressure_sys >= 130 or blood_pressure_dia >= 80:
            risk_score += 10

        # Cholesterol (general guidelines)
        if cholesterol >= 240:
            risk_score += 15
        elif cholesterol >= 200:
            risk_score += 8

        # Blood sugar (diabetes screening)
        if blood_sugar >= 126:
            risk_score += 20
        elif blood_sugar >= 100:
            risk_score += 10

        # Age factor
        if age >= 65:
            risk_score += 10
        elif age >= 50:
            risk_score += 5

        return min(risk_score, 100)

    def adjust_for_fitness_goal(self, tdee, goal, timeline):
        """Adjust calories based on fitness goal and timeline"""
        if not self.config:
            raise ValueError("Configuration not loaded. Please call load_model() first.")
        
        adjustments = self.config['nutrition']['goal_adjustments']
        adjustment = adjustments.get(goal, {}).get(timeline, 0)
        return tdee + adjustment

    def calculate_macro_ratios(self, goal, dietary_preference):
        """Calculate protein/carb/fat ratios based on goal and diet"""
        if not self.config:
            raise ValueError("Configuration not loaded. Please call load_model() first.")
        
        # Get base ratios from config
        goal_ratios = self.config['nutrition']['macro_ratios']
        base_ratios = goal_ratios.get(goal, goal_ratios['maintenance'])
        
        protein_pct = base_ratios['protein_percent'] / 100
        carb_pct = base_ratios['carbs_percent'] / 100
        fat_pct = base_ratios['fats_percent'] / 100
        
        # Adjust for dietary preferences
        dietary_adj = self.config['nutrition']['dietary_adjustments']
        
        if dietary_preference in ['vegan', 'vegetarian'] and dietary_preference in dietary_adj:
            adj = dietary_adj[dietary_preference]
            protein_pct = max(0.20, protein_pct + adj['protein_adjustment'] / 100)
            carb_pct += adj['carbs_adjustment'] / 100
        elif dietary_preference == 'keto' and 'keto' in dietary_adj:
            keto = dietary_adj['keto']
            protein_pct = keto['protein_percent'] / 100
            carb_pct = keto['carbs_percent'] / 100
            fat_pct = keto['fats_percent'] / 100
            
        return protein_pct, carb_pct, fat_pct

    def calculate_meal_distribution(self, total_calories, protein_g, carbs_g, fats_g, meal_frequency, timing_preference):
        """Distribute macros across meals based on frequency and timing"""
        if not self.config:
            raise ValueError("Configuration not loaded. Please call load_model() first.")
        
        meals = []
        
        # Get meal distribution from config
        meal_key = f"{meal_frequency}_meals"
        distributions = self.config['nutrition']['meal_distributions']
        
        if meal_key not in distributions:
            raise ValueError(f"Meal frequency {meal_frequency} not supported. Use 2-6 meals.")
        
        meal_config = distributions[meal_key]
        meal_names = meal_config['meal_names']
        
        # Get percentages based on timing preference
        timing_key = timing_preference if timing_preference in meal_config else 'balanced'
        percentages = [p / 100 for p in meal_config[timing_key]]
        
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
        if not self.config:
            raise ValueError("Configuration not loaded. Please call load_model() first.")
        
        bounds = self.config['nutrition']['safety_bounds']
        
        min_calories = bmr * bounds['min_calorie_multiplier']
        max_calories = bmr * bounds['max_calorie_multiplier']
        safe_calories = np.clip(calories, min_calories, max_calories)

        approx_weight = bmr / 15
        min_protein = approx_weight * bounds['min_protein_per_kg']
        max_protein = approx_weight * bounds['max_protein_per_kg']
        safe_protein = np.clip(protein, min_protein, max_protein)

        total_macro_calories = safe_protein * 4 + carbs * 4 + fats * 9

        if total_macro_calories > safe_calories * bounds['macro_tolerance']:
            scale_factor = safe_calories / total_macro_calories
            safe_protein *= scale_factor
            carbs *= scale_factor
            fats *= scale_factor

        return safe_calories, safe_protein, carbs, fats

    def predict(self, user_data):
        """Make prediction for a single user with enhanced personalization"""
        if self.model is None:
            raise ValueError("Model not trained yet!")
        
        if not self.config:
            raise ValueError("Configuration not loaded. Please call load_model() with config parameter.")

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

    def load_model(self, filename='enhanced_diet_predictor.pkl', config=None):
        """Load a trained model and configuration"""
        self.model, self.feature_names, self.target_names = joblib.load(filename)
        if config:
            self.config = config
        print(f"✅ Enhanced model loaded from '{filename}'")
