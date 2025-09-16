# 🚀 Quick Start Guide - Gymbite ML Model

## ⚡ Fastest Way to Run

### 1. Install Dependencies
```bash
pip install numpy pandas scikit-learn matplotlib joblib
```

### 2. Run the Demo
```bash
python simple_enhanced_demo.py
```

**That's it!** 🎉 You'll see:
- Model training with 97% accuracy
- Feature engineering demonstration  
- Sample predictions for 2 users
- **🍽️ Complete personalized meal plans with specific food recommendations**
- Nutrition breakdowns and health tips

## 🍽️ Get Just the Meal Plan
```bash
python meal_plan_generator.py
```
**Perfect for**: Getting meal recommendations without training details

## 🔄 Alternative Options

### Train Fresh Model
```bash
python enhanced_diet_model.py
```

### Use Pre-trained Model
```python
from enhanced_diet_model import EnhancedDietPredictor

predictor = EnhancedDietPredictor()
predictor.load_model()

# Your data
user_data = {
    'Age': 25, 'Gender': 'Male', 'Height_cm': 180, 'Weight_kg': 80,
    'BMI': 24.7, 'Exercise_Frequency': 4, 'Daily_Steps': 8000,
    'Blood_Pressure_Systolic': 120, 'Blood_Pressure_Diastolic': 75,
    'Cholesterol_Level': 170, 'Blood_Sugar_Level': 90, 'Sleep_Hours': 8,
    'Caloric_Intake': 2500, 'Protein_Intake': 100,
    'Carbohydrate_Intake': 300, 'Fat_Intake': 80
}

# Get prediction
result = predictor.predict(user_data)
print(f"Recommended Calories: {result['recommended_calories']} kcal")
```

## 📋 Requirements
- Python 3.8+
- 5 packages: numpy, pandas, scikit-learn, matplotlib, joblib
- Dataset included: `Personalized_Diet_Recommendations.csv`

## ✅ Expected Results
- **Calorie prediction**: 97% accuracy (R² = 0.968)
- **Complete nutrition**: Protein, carbs, fats with safety validation
- **Health insights**: BMR, TDEE, risk assessment
