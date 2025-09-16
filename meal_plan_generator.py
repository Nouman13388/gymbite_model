"""
Standalone Meal Plan Generator
Get personalized meal recommendations based on your health data
"""

from enhanced_diet_model import EnhancedDietPredictor
import numpy as np

def generate_meal_plan(prediction, user_name="User"):
    """Generate a sample meal plan based on nutrition predictions"""
    calories = prediction['recommended_calories']
    protein = prediction['recommended_protein']
    carbs = prediction['recommended_carbs']
    fats = prediction['recommended_fats']
    
    # Meal distribution percentages
    meals = {
        "🌅 Breakfast": {"pct": 0.25, "calories": round(calories * 0.25), "protein": round(protein * 0.25, 1), "carbs": round(carbs * 0.25, 1), "fats": round(fats * 0.25, 1)},
        "🍽️ Lunch": {"pct": 0.35, "calories": round(calories * 0.35), "protein": round(protein * 0.35, 1), "carbs": round(carbs * 0.35, 1), "fats": round(fats * 0.35, 1)},
        "🌙 Dinner": {"pct": 0.30, "calories": round(calories * 0.30), "protein": round(protein * 0.30, 1), "carbs": round(carbs * 0.30, 1), "fats": round(fats * 0.30, 1)},
        "🍎 Snacks": {"pct": 0.10, "calories": round(calories * 0.10), "protein": round(protein * 0.10, 1), "carbs": round(carbs * 0.10, 1), "fats": round(fats * 0.10, 1)}
    }
    
    # Sample food recommendations
    meal_suggestions = {
        "🌅 Breakfast": [
            "• Oatmeal (1 cup) + Greek yogurt (1 cup) + Berries + Almonds",
            "• Scrambled eggs (3 eggs) + Whole grain toast + Avocado",
            "• Protein smoothie (protein powder + banana + oats + peanut butter)"
        ],
        "🍽️ Lunch": [
            "• Grilled chicken breast (150g) + Brown rice (1 cup) + Mixed vegetables",
            "• Salmon fillet (150g) + Quinoa (1 cup) + Green salad with olive oil",
            "• Turkey sandwich (whole grain bread) + Side salad + Apple"
        ],
        "🌙 Dinner": [
            "• Lean beef (120g) + Sweet potato + Steamed broccoli",
            "• Baked cod (150g) + Wild rice + Asparagus",
            "• Tofu stir-fry with vegetables + Brown rice"
        ],
        "🍎 Snacks": [
            "• Greek yogurt + Mixed nuts",
            "• Apple with almond butter",
            "• Protein bar + Banana"
        ]
    }
    
    return meals, meal_suggestions

def display_meal_plan(prediction, user_name="User"):
    """Display a complete meal plan recommendation"""
    meals, meal_suggestions = generate_meal_plan(prediction, user_name)
    
    print(f"\n🍽️ PERSONALIZED MEAL PLAN for {user_name}")
    print("=" * 50)
    
    for meal_name, nutrition in meals.items():
        print(f"\n{meal_name}")
        print(f"  📊 Target: {nutrition['calories']} kcal | {nutrition['protein']}g protein | {nutrition['carbs']}g carbs | {nutrition['fats']}g fats")
        print(f"  💡 Meal Ideas:")
        for suggestion in meal_suggestions[meal_name]:
            print(f"    {suggestion}")
    
    print(f"\n📋 DAILY SUMMARY")
    print(f"  🎯 Total Target: {prediction['recommended_calories']} kcal")
    print(f"  🥩 Protein: {prediction['recommended_protein']}g ({(prediction['recommended_protein']*4/prediction['recommended_calories']*100):.1f}%)")
    print(f"  🍞 Carbs: {prediction['recommended_carbs']}g ({(prediction['recommended_carbs']*4/prediction['recommended_calories']*100):.1f}%)")
    print(f"  🥑 Fats: {prediction['recommended_fats']}g ({(prediction['recommended_fats']*9/prediction['recommended_calories']*100):.1f}%)")

def get_user_meal_plan():
    """Interactive meal plan generator"""
    print("🍽️ PERSONALIZED MEAL PLAN GENERATOR")
    print("=" * 40)
    
    # Load the trained model
    try:
        predictor = EnhancedDietPredictor()
        predictor.load_model()
        print("✅ Model loaded successfully!")
    except:
        print("❌ Error: Could not load model. Run 'python enhanced_diet_model.py' first.")
        return
    
    # Example user data (you can modify this or make it interactive)
    print("\n📝 Using sample user data (modify the code to input your own):")
    
    user_data = {
        'Age': 28, 'Gender': 'Female', 'Height_cm': 165, 'Weight_kg': 75,
        'BMI': 27.5, 'Blood_Pressure_Systolic': 125, 'Blood_Pressure_Diastolic': 80,
        'Cholesterol_Level': 180, 'Blood_Sugar_Level': 95, 'Daily_Steps': 10000,
        'Exercise_Frequency': 5, 'Sleep_Hours': 7.5, 'Caloric_Intake': 2200,
        'Protein_Intake': 80, 'Carbohydrate_Intake': 250, 'Fat_Intake': 70
    }
    
    print(f"👤 User: {user_data['Age']}yr {user_data['Gender']}, {user_data['Weight_kg']}kg, {user_data['Exercise_Frequency']}x/week exercise")
    
    # Get prediction
    try:
        prediction = predictor.predict(user_data)
        print("\n✅ Nutrition prediction successful!")
        
        # Display the meal plan
        display_meal_plan(prediction, f"{user_data['Age']}yr {user_data['Gender']}")
        
        print("\n💡 CUSTOMIZATION TIPS:")
        print("  • Adjust portion sizes based on hunger and activity")
        print("  • Swap similar foods (chicken ↔ fish, rice ↔ quinoa)")
        print("  • Include variety of colorful vegetables")
        print("  • Stay hydrated with water throughout the day")
        
    except Exception as e:
        print(f"❌ Error making prediction: {e}")

if __name__ == "__main__":
    get_user_meal_plan()
