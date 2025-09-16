"""
Simple Enhanced Gymbite Model - Core ML Only
Demonstrates the improvements without GUI/API complexity
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error
import joblib

def calculate_bmr(age, weight, height, gender):
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation"""
    if gender.lower() == 'male':
        return 10 * weight + 6.25 * height - 5 * age + 5
    elif gender.lower() == 'female':
        return 10 * weight + 6.25 * height - 5 * age - 161
    else:  # Other
        return 10 * weight + 6.25 * height - 5 * age - 78

def calculate_tdee(bmr, exercise_frequency, daily_steps):
    """Calculate Total Daily Energy Expenditure"""
    if exercise_frequency >= 6:
        activity_multiplier = 1.725  # Very active
    elif exercise_frequency >= 4:
        activity_multiplier = 1.55   # Moderately active
    elif exercise_frequency >= 2:
        activity_multiplier = 1.375  # Lightly active
    else:
        activity_multiplier = 1.2    # Sedentary
    
    # Adjust based on daily steps
    if daily_steps > 12000:
        activity_multiplier += 0.1
    elif daily_steps > 8000:
        activity_multiplier += 0.05
    
    return bmr * activity_multiplier

def calculate_health_risk_score(bmi, bp_sys, bp_dia, cholesterol, blood_sugar, age):
    """Calculate health risk score (0-100, higher = more risk)"""
    risk = 0
    
    # BMI risk
    if bmi >= 30: risk += 25
    elif bmi >= 25: risk += 15
    elif bmi < 18.5: risk += 10
    
    # Blood pressure risk
    if bp_sys >= 140 or bp_dia >= 90: risk += 20
    elif bp_sys >= 130 or bp_dia >= 80: risk += 10
    
    # Cholesterol risk
    if cholesterol >= 240: risk += 15
    elif cholesterol >= 200: risk += 8
    
    # Blood sugar risk
    if blood_sugar >= 126: risk += 20
    elif blood_sugar >= 100: risk += 10
    
    # Age risk
    if age >= 65: risk += 10
    elif age >= 50: risk += 5
    
    return min(risk, 100)

def enhance_dataset(df):
    """Add calculated features to make the model smarter"""
    print("🔧 Adding intelligent features...")
    
    df_enhanced = df.copy()
    
    # Calculate BMR for each person
    df_enhanced['BMR'] = df_enhanced.apply(
        lambda row: calculate_bmr(row['Age'], row['Weight_kg'], row['Height_cm'], row['Gender']), 
        axis=1
    )
    
    # Calculate TDEE (total daily energy expenditure)
    df_enhanced['TDEE'] = df_enhanced.apply(
        lambda row: calculate_tdee(row['BMR'], row['Exercise_Frequency'], row['Daily_Steps']), 
        axis=1
    )
    
    # Calculate health risk score
    df_enhanced['Health_Risk_Score'] = df_enhanced.apply(
        lambda row: calculate_health_risk_score(
            row['BMI'], row['Blood_Pressure_Systolic'], row['Blood_Pressure_Diastolic'],
            row['Cholesterol_Level'], row['Blood_Sugar_Level'], row['Age']
        ), axis=1
    )
    
    # Activity level score (0-10)
    df_enhanced['Activity_Level_Score'] = (
        (df_enhanced['Exercise_Frequency'] / 7) * 5 + 
        (np.clip(df_enhanced['Daily_Steps'] / 15000, 0, 1)) * 5
    )
    
    print(f"✅ Added 4 intelligent features: BMR, TDEE, Health_Risk_Score, Activity_Level_Score")
    return df_enhanced

def train_enhanced_model(df):
    """Train the enhanced multi-output model"""
    print("\n🤖 Training Enhanced Model")
    print("=" * 40)
    
    # Enhance dataset with smart features
    df_enhanced = enhance_dataset(df)
    
    # Prepare features and targets
    numeric_df = df_enhanced.select_dtypes(include=[np.number])
    
    # Features (everything except targets and ID)
    feature_cols = [col for col in numeric_df.columns 
                   if not col.startswith('Recommended_') and col != 'Patient_ID']
    X = numeric_df[feature_cols]
    
    # Multiple targets (calories, protein, carbs, fats)
    target_cols = ['Recommended_Calories', 'Recommended_Protein', 
                   'Recommended_Carbs', 'Recommended_Fats']
    y = numeric_df[target_cols]
    
    print(f"📊 Features: {len(feature_cols)} (including {['BMR', 'TDEE', 'Health_Risk_Score', 'Activity_Level_Score']})")
    print(f"🎯 Targets: {len(target_cols)} (Calories, Protein, Carbs, Fats)")
    
    # Train-test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train multi-output model
    base_model = RandomForestRegressor(n_estimators=100, random_state=42)
    model = MultiOutputRegressor(base_model)
    model.fit(X_train, y_train)
      # Evaluate with comprehensive accuracy metrics
    y_pred = model.predict(X_test)
    
    print(f"\n📈 Model Performance & Accuracy:")
    print("=" * 45)
    
    overall_accuracies = []
    
    for i, target in enumerate(target_cols):
        y_true = y_test.iloc[:, i]
        y_pred_single = y_pred[:, i]
        
        # Calculate metrics
        r2 = r2_score(y_true, y_pred_single)
        mae = mean_absolute_error(y_true, y_pred_single)
        
        # Calculate percentage accuracy (within 10% tolerance)
        percentage_error = np.abs((y_true - y_pred_single) / y_true) * 100
        accuracy_10pct = np.mean(percentage_error <= 10) * 100
        overall_accuracies.append(accuracy_10pct)
        
        print(f"  {target}: R² = {r2:.3f}, MAE = {mae:.1f}, Accuracy = {accuracy_10pct:.1f}%")
    
    # Overall accuracy
    overall_accuracy = np.mean(overall_accuracies)
    print(f"\n🏆 Overall Model Accuracy: {overall_accuracy:.1f}% (±10% tolerance)")
    print(f"📊 Quality Rating: {'Excellent' if overall_accuracy > 90 else 'Good' if overall_accuracy > 80 else 'Fair'}")
    
    # Save model
    joblib.dump((model, feature_cols, target_cols), 'simple_enhanced_model.pkl')
    print(f"\n✅ Model saved as 'simple_enhanced_model.pkl'")
    
    return model, feature_cols, target_cols

def predict_nutrition(user_data, model, feature_cols):
    """Make a single prediction"""
    # Calculate derived features for the user
    bmr = calculate_bmr(user_data['Age'], user_data['Weight_kg'], 
                       user_data['Height_cm'], user_data['Gender'])
    
    tdee = calculate_tdee(bmr, user_data['Exercise_Frequency'], user_data['Daily_Steps'])
    
    health_risk = calculate_health_risk_score(
        user_data['BMI'], user_data['Blood_Pressure_Systolic'],
        user_data['Blood_Pressure_Diastolic'], user_data['Cholesterol_Level'],
        user_data['Blood_Sugar_Level'], user_data['Age']
    )
    
    activity_score = (user_data['Exercise_Frequency'] / 7) * 5 + \
                    (np.clip(user_data['Daily_Steps'] / 15000, 0, 1)) * 5
    
    # Add calculated features to user data
    enhanced_user_data = user_data.copy()
    enhanced_user_data.update({
        'BMR': bmr,
        'TDEE': tdee,
        'Health_Risk_Score': health_risk,
        'Activity_Level_Score': activity_score
    })
    
    # Create feature vector in correct order
    user_features = [enhanced_user_data[col] for col in feature_cols]
    user_df = pd.DataFrame([user_features], columns=feature_cols)
    
    # Make prediction
    prediction = model.predict(user_df)[0]
    
    # Apply safety validation
    min_calories = bmr * 0.8  # Never below 80% of BMR
    max_calories = bmr * 2.0  # Never above 200% of BMR
    safe_calories = np.clip(prediction[0], min_calories, max_calories)
    
    return {
        'calories': round(safe_calories),
        'protein': round(prediction[1], 1),
        'carbs': round(prediction[2], 1),
        'fats': round(prediction[3], 1),
        'bmr': round(bmr),
        'tdee': round(tdee),
        'health_risk': round(health_risk),
        'activity_level': round(activity_score, 1)
    }

def generate_meal_plan(prediction, user_name="User"):
    """Generate a sample meal plan based on nutrition predictions"""
    calories = prediction['calories']
    protein = prediction['protein']
    carbs = prediction['carbs']
    fats = prediction['fats']
    
    # Meal distribution percentages
    breakfast_pct = 0.25  # 25% of daily nutrition
    lunch_pct = 0.35      # 35% of daily nutrition
    dinner_pct = 0.30     # 30% of daily nutrition
    snacks_pct = 0.10     # 10% of daily nutrition
    
    # Calculate nutrition per meal
    meals = {
        "🌅 Breakfast": {
            "calories": round(calories * breakfast_pct),
            "protein": round(protein * breakfast_pct, 1),
            "carbs": round(carbs * breakfast_pct, 1),
            "fats": round(fats * breakfast_pct, 1)
        },
        "🍽️ Lunch": {
            "calories": round(calories * lunch_pct),
            "protein": round(protein * lunch_pct, 1),
            "carbs": round(carbs * lunch_pct, 1),
            "fats": round(fats * lunch_pct, 1)
        },
        "🌙 Dinner": {
            "calories": round(calories * dinner_pct),
            "protein": round(protein * dinner_pct, 1),
            "carbs": round(carbs * dinner_pct, 1),
            "fats": round(fats * dinner_pct, 1)
        },
        "🍎 Snacks": {
            "calories": round(calories * snacks_pct),
            "protein": round(protein * snacks_pct, 1),
            "carbs": round(carbs * snacks_pct, 1),
            "fats": round(fats * snacks_pct, 1)
        }
    }
    
    # Sample food recommendations based on macro targets
    food_database = {
        "high_protein": ["Chicken breast", "Greek yogurt", "Eggs", "Salmon", "Tofu", "Lean beef", "Cottage cheese"],
        "high_carbs": ["Oatmeal", "Brown rice", "Sweet potato", "Quinoa", "Whole wheat bread", "Fruits", "Pasta"],
        "high_fats": ["Avocado", "Nuts", "Olive oil", "Seeds", "Nut butter", "Fatty fish"],
        "balanced": ["Mixed vegetables", "Salad", "Soup", "Smoothie"]
    }
    
    # Generate meal suggestions
    meal_plans = {
        "🌅 Breakfast": [
            f"• {food_database['high_carbs'][0]} with {food_database['high_protein'][1]}",
            f"• {food_database['high_protein'][2]} with {food_database['high_carbs'][5]}",
            f"• {food_database['balanced'][3]} with {food_database['high_protein'][1]}"
        ],
        "🍽️ Lunch": [
            f"• {food_database['high_protein'][0]} with {food_database['high_carbs'][1]}",
            f"• {food_database['high_protein'][3]} with {food_database['high_carbs'][3]}",
            f"• {food_database['balanced'][1]} with {food_database['high_protein'][5]}"
        ],
        "🌙 Dinner": [
            f"• {food_database['high_protein'][5]} with {food_database['high_carbs'][2]}",
            f"• {food_database['high_protein'][4]} with {food_database['high_carbs'][6]}",
            f"• {food_database['high_protein'][3]} with {food_database['balanced'][0]}"
        ],
        "🍎 Snacks": [
            f"• {food_database['high_fats'][1]} with {food_database['high_carbs'][5]}",
            f"• {food_database['high_protein'][6]} with {food_database['balanced'][0]}",
            f"• {food_database['high_fats'][4]} with {food_database['high_carbs'][4]}"
        ]
    }
    
    return meals, meal_plans

def display_meal_plan(prediction, user_name="User"):
    """Display a complete meal plan recommendation"""
    meals, meal_plans = generate_meal_plan(prediction, user_name)
    
    print(f"\n🍽️ PERSONALIZED MEAL PLAN for {user_name}")
    print("=" * 50)
    
    for meal_name, nutrition in meals.items():
        print(f"\n{meal_name}")
        print(f"  📊 Target: {nutrition['calories']} kcal | {nutrition['protein']}g protein | {nutrition['carbs']}g carbs | {nutrition['fats']}g fats")
        print(f"  💡 Suggestions:")
        for suggestion in meal_plans[meal_name]:
            print(f"    {suggestion}")
    
    print(f"\n📋 DAILY SUMMARY")
    print(f"  🎯 Total Daily Target: {prediction['calories']} kcal")
    print(f"  🥩 Protein: {prediction['protein']}g ({(prediction['protein']*4/prediction['calories']*100):.1f}%)")
    print(f"  🍞 Carbs: {prediction['carbs']}g ({(prediction['carbs']*4/prediction['calories']*100):.1f}%)")
    print(f"  🥑 Fats: {prediction['fats']}g ({(prediction['fats']*9/prediction['calories']*100):.1f}%)")
    
    # Additional tips based on goals
    if prediction['health_risk'] > 50:
        print(f"\n⚠️ HEALTH-FOCUSED TIPS:")
        print(f"  • Focus on whole foods, limit processed items")
        print(f"  • Increase vegetables and lean proteins")
        print(f"  • Consider consulting with a healthcare provider")
    elif prediction['activity_level'] > 7:
        print(f"\n💪 PERFORMANCE TIPS:")
        print(f"  • Time carbs around workouts for energy")
        print(f"  • Include protein post-workout for recovery")
        print(f"  • Stay hydrated, especially during exercise")
    else:
        print(f"\n🌱 GENERAL WELLNESS TIPS:")
        print(f"  • Focus on balanced meals with all macros")
        print(f"  • Include variety of colorful vegetables")
        print(f"  • Maintain consistent meal timing")

def demo_comparison():
    """Demo showing original vs enhanced approach"""
    print("🎯 GYMBITE MODEL COMPARISON DEMO")
    print("=" * 50)
    
    # Load dataset
    df = pd.read_csv('Personalized_Diet_Recommendations.csv')
    print(f"📁 Dataset loaded: {len(df)} records")
    
    # Train enhanced model
    model, feature_cols, target_cols = train_enhanced_model(df)
    
    # Test user examples
    test_users = [
        {
            "name": "🏃‍♀️ Sarah (28F, Active, Weight Loss Goal)",
            "data": {
                'Age': 28, 'Gender': 'Female', 'Height_cm': 165, 'Weight_kg': 75, 'BMI': 27.5,
                'Blood_Pressure_Systolic': 125, 'Blood_Pressure_Diastolic': 80,
                'Cholesterol_Level': 180, 'Blood_Sugar_Level': 95, 'Daily_Steps': 10000,
                'Exercise_Frequency': 5, 'Sleep_Hours': 7.5, 'Caloric_Intake': 2200,
                'Protein_Intake': 80, 'Carbohydrate_Intake': 250, 'Fat_Intake': 70
            }
        },
        {
            "name": "💪 Mike (25M, Very Active, Muscle Gain)",
            "data": {
                'Age': 25, 'Gender': 'Male', 'Height_cm': 180, 'Weight_kg': 70, 'BMI': 21.6,
                'Blood_Pressure_Systolic': 120, 'Blood_Pressure_Diastolic': 75,
                'Cholesterol_Level': 160, 'Blood_Sugar_Level': 85, 'Daily_Steps': 12000,
                'Exercise_Frequency': 6, 'Sleep_Hours': 8.0, 'Caloric_Intake': 2800,
                'Protein_Intake': 120, 'Carbohydrate_Intake': 300, 'Fat_Intake': 80
            }
        }
    ]
    
    print(f"\n🔮 ENHANCED PREDICTIONS")
    print("=" * 30)
    
    for user in test_users:
        print(f"\n{user['name']}")
        print("-" * 40)
        
        prediction = predict_nutrition(user['data'], model, feature_cols)
        
        print(f"🎯 Complete Nutrition Plan:")
        print(f"  🔥 Calories: {prediction['calories']} kcal")
        print(f"  🥩 Protein: {prediction['protein']} g")
        print(f"  🍞 Carbs: {prediction['carbs']} g")
        print(f"  🥑 Fats: {prediction['fats']} g")
        
        print(f"\n📊 Intelligent Insights:")
        print(f"  BMR (resting metabolism): {prediction['bmr']} kcal")
        print(f"  TDEE (total daily burn): {prediction['tdee']} kcal")
        print(f"  Health risk score: {prediction['health_risk']}/100")
        print(f"  Activity level: {prediction['activity_level']}/10")
        
        # Calculate macro percentages
        total_cal = prediction['calories']
        protein_pct = (prediction['protein'] * 4 / total_cal) * 100
        carbs_pct = (prediction['carbs'] * 4 / total_cal) * 100
        fats_pct = (prediction['fats'] * 9 / total_cal) * 100
        
        print(f"\n🥧 Macro Distribution:")
        print(f"  Protein: {protein_pct:.1f}% (muscle building)")
        print(f"  Carbs: {carbs_pct:.1f}% (energy)")
        print(f"  Fats: {fats_pct:.1f}% (hormones, vitamins)")        # Health recommendations
        if prediction['health_risk'] < 25:
            print(f"✅ Health Status: Excellent!")
        elif prediction['health_risk'] < 50:
            print(f"💡 Health Tip: Focus on reducing risk factors")
        else:
            print(f"⚠️ Health Alert: Consider consulting healthcare provider")
        
        # Display meal plan for this user
        display_meal_plan(prediction, user['name'])

if __name__ == "__main__":
    demo_comparison()
