"""
Test script for enhanced Gymbite API with user preferences
Tests the new functionality without requiring Gemini API key
"""

import sys
import json

# Test that imports work
try:
    from app import Input, MealPlanRequest
    from enhanced_diet_model import EnhancedDietPredictor
    print("✅ All imports successful")
except ImportError as e:
    print(f"❌ Import error: {e}")
    sys.exit(1)

# Test 1: Validate Input schema with new fields
print("\n--- Test 1: Input Schema Validation ---")
try:
    test_input = Input(
        # Health data
        Age=28,
        Gender="Male",
        Height_cm=180.0,
        Weight_kg=85.0,
        BMI=26.2,
        Exercise_Frequency=5,
        Daily_Steps=12000,
        Blood_Pressure_Systolic=120,
        Blood_Pressure_Diastolic=80,
        Cholesterol_Level=180,
        Blood_Sugar_Level=90,
        Sleep_Hours=7.5,
        Caloric_Intake=2800,
        Protein_Intake=150,
        Carbohydrate_Intake=300,
        Fat_Intake=80,
        # User preferences
        Region="Pakistan",
        City="Lahore",
        Dietary_Preference="halal",
        Fitness_Goal="muscle_gain",
        Goal_Timeline="moderate",
        Meal_Frequency=4,
        Excluded_Ingredients=["beef"],
        Allergens=["peanuts"],
        Budget_Level="medium",
        Cooking_Time="moderate",
        Cuisine_Preference="local",
        Meal_Timing_Preference="balanced"
    )
    print("✅ Input schema accepts all new preference fields")
    print(f"   Region: {test_input.Region}")
    print(f"   Dietary Preference: {test_input.Dietary_Preference}")
    print(f"   Fitness Goal: {test_input.Fitness_Goal}")
except Exception as e:
    print(f"❌ Input validation failed: {e}")
    sys.exit(1)

# Test 2: Test new model functions
print("\n--- Test 2: Enhanced Model Functions ---")
try:
    predictor = EnhancedDietPredictor()
    
    # Test fitness goal adjustment
    tdee = 2500
    adjusted = predictor.adjust_for_fitness_goal(tdee, "muscle_gain", "moderate")
    print(f"✅ Fitness goal adjustment: TDEE {tdee} → {adjusted} cal (muscle gain, moderate)")
    
    # Test macro ratio calculation
    protein_pct, carb_pct, fat_pct = predictor.calculate_macro_ratios("muscle_gain", "halal")
    print(f"✅ Macro ratios (muscle gain): P{protein_pct*100:.0f}% C{carb_pct*100:.0f}% F{fat_pct*100:.0f}%")
    
    # Test meal distribution
    meals = predictor.calculate_meal_distribution(2400, 180, 270, 67, 4, "balanced")
    print(f"✅ Meal distribution: {len(meals)} meals")
    for meal in meals:
        print(f"   {meal['meal']}: {meal['calories']} cal")
    
    # Test dietary constraints builder
    constraints = predictor.build_dietary_constraints(test_input.model_dump())
    print(f"✅ Dietary constraints built:")
    print(f"   Region: {constraints['region']}")
    print(f"   Allergens: {constraints['allergens']}")
    
except Exception as e:
    print(f"❌ Model function test failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Test MealPlanRequest schema
print("\n--- Test 3: MealPlanRequest Schema ---")
try:
    meal_request = MealPlanRequest(
        total_calories=2400,
        total_protein=180,
        total_carbs=270,
        total_fats=67,
        meals=[
            {"meal": "Breakfast", "calories": 600, "protein": 45, "carbs": 67, "fats": 17},
            {"meal": "Lunch", "calories": 600, "protein": 45, "carbs": 67, "fats": 17}
        ],
        region="Pakistan",
        city="Lahore",
        dietary_preference="halal",
        excluded_ingredients=["beef"],
        allergens=["peanuts"],
        budget_level="medium",
        cooking_time="moderate",
        cuisine_preference="local"
    )
    print("✅ MealPlanRequest schema validated")
    print(f"   Total calories: {meal_request.total_calories}")
    print(f"   Meals: {len(meal_request.meals)}")
except Exception as e:
    print(f"❌ MealPlanRequest validation failed: {e}")
    sys.exit(1)

print("\n" + "="*50)
print("🎉 ALL TESTS PASSED!")
print("="*50)
print("\nNext steps:")
print("1. Set GEMINI_API_KEY environment variable")
print("2. Run: uvicorn app:app --reload")
print("3. Test /predict endpoint with enhanced input")
print("4. Test /generate-meal-plan endpoint")
