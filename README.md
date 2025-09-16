# 🏋️ Gymbite ML Model

A machine learning system for personalized nutrition recommendations using **Multi-Output Regression** with advanced feature engineering and safety validation.

## 🎯 ML Techniques & Architecture

### **1. Multi-Output Regression**
```python
from sklearn.multioutput import MultiOutputRegressor
from sklearn.ensemble import RandomForestRegressor

# Predicts 4 targets simultaneously: [Calories, Protein, Carbs, Fats]
model = MultiOutputRegressor(RandomForestRegressor(n_estimators=100, random_state=42))
```

### **2. Feature Engineering**
- **Metabolic Features**: BMR (Basal Metabolic Rate), TDEE (Total Daily Energy Expenditure)
- **Health Risk Scoring**: Composite risk assessment (0-100)
- **Activity Profiling**: Exercise frequency + daily steps integration

### **3. Safety Validation**
- Nutritional bounds validation (80-200% of BMR)
- Macro distribution constraints
- Health risk-based adjustments

## 📁 Project Structure

```
gymbite_model/
├── enhanced_diet_model.py            # Main ML model
├── simple_enhanced_demo.py           # Demo script with meal plans
├── meal_plan_generator.py            # Standalone meal plan generator
├── Personalized_Diet_Recommendations.csv  # Dataset (5000 records)
├── enhanced_diet_predictor.pkl       # Trained model
├── enhanced_feature_importance.png   # Feature analysis
└── requirements.txt                  # Dependencies
```

## 🧠 Machine Learning Pipeline

### **Step 1: Feature Engineering**
```python
def enhance_dataset(self, df):
    # Metabolic calculations
    df['BMR'] = self.calculate_bmr(age, weight, height, gender)  # Mifflin-St Jeor Equation
    df['TDEE'] = self.calculate_tdee(bmr, exercise_freq, steps)  # Activity multipliers
    df['Health_Risk'] = self.calculate_health_risk_score(...)   # Composite risk (0-100)
    
    # Activity profiling
    df['Activity_Level'] = self.categorize_activity_level(exercise_freq)
    df['Steps_Category'] = pd.cut(daily_steps, bins=[0, 5000, 10000, 15000, float('inf')])
    
    return df  # 19 engineered features vs 13 original
```

### **Step 2: Multi-Output Training**
```python
# Target variables: 4 simultaneous predictions
targets = ['Recommended_Calories', 'Recommended_Protein', 'Recommended_Carbs', 'Recommended_Fats']

# Random Forest with Multi-Output wrapper
model = MultiOutputRegressor(RandomForestRegressor(
    n_estimators=100,
    max_depth=15,
    min_samples_split=5,
    random_state=42
))

# Train on enhanced features
model.fit(X_enhanced, y_multi)
```

### **Step 3: Safety Validation**
```python
def validate_prediction(self, calories, protein, carbs, fats, bmr):
    # Metabolic safety bounds
    min_calories = bmr * 0.8  # Below this = starvation
    max_calories = bmr * 2.0  # Above this = excessive gain
    
    # Macro distribution validation
    protein_ratio = (protein * 4) / calories  # Should be 10-35%
    carb_ratio = (carbs * 4) / calories       # Should be 45-65%
    fat_ratio = (fats * 9) / calories         # Should be 20-35%
    
    return safe_values
```

## 📈 Model Performance

| Metric | Value | Technique |
|--------|-------|-----------|
| **Calorie Prediction** | R² = 0.968, MAE = 102 kcal | Multi-Output Random Forest |
| **Protein Prediction** | R² = 0.960, MAE = 7.6g | Feature Engineering (BMR/TDEE) |
| **Carb Prediction** | R² = 0.890, MAE = 25.9g | Activity Level Profiling |
| **Fat Prediction** | R² = 0.944, MAE = 7.8g | Health Risk Integration |

**Key ML Improvements:**
- **Feature Engineering**: 19 calculated features vs 13 raw features (+46% data richness)
- **Multi-Output Learning**: 4 simultaneous predictions vs 1 single output
- **Safety Constraints**: Built-in validation prevents dangerous recommendations

## 🚀 Step-by-Step Instructions to Run

### **Step 1: Prerequisites**
- Python 3.8 or higher installed
- Command prompt or terminal access

### **Step 2: Install Dependencies**
```bash
# Install required packages
pip install numpy pandas scikit-learn matplotlib joblib
```

### **Step 3: Run the Model (3 Options)**

#### **Option A: Quick Demo with Meal Plans (Recommended)**
```bash
# Run the complete demonstration with meal recommendations
python simple_enhanced_demo.py
```
**What it does:**
- Loads the dataset (5000 nutrition records)
- Trains the enhanced model with feature engineering
- Shows performance metrics (97% accuracy)
- Demonstrates predictions for 2 sample users
- **🍽️ Generates personalized meal plans with specific food recommendations**
- Saves the trained model

#### **Option B: Generate Meal Plan Only**
```bash
# Get meal plan for sample user
python meal_plan_generator.py
```
**What it does:**
- Loads pre-trained model
- Predicts nutrition for sample user
- **🍽️ Shows detailed meal plan with breakfast, lunch, dinner, snacks**
- Provides food suggestions and customization tips

#### **Option C: Train Your Own Model**
```bash
# Train and evaluate the enhanced model
python enhanced_diet_model.py
```
**What it does:**
- Full model training with detailed logging
- Feature importance analysis
- Model evaluation and saving
- Generates feature importance visualization

#### **Option D: Use Pre-trained Model Programmatically**
```python
# Load and use the existing trained model
from enhanced_diet_model import EnhancedDietPredictor

predictor = EnhancedDietPredictor()
predictor.load_model()  # Loads enhanced_diet_predictor.pkl

# Make prediction for your data
user_data = {
    'Age': 28, 'Gender': 'Female', 'Height_cm': 165, 'Weight_kg': 75,
    'BMI': 27.5, 'Exercise_Frequency': 5, 'Daily_Steps': 10000,
    'Blood_Pressure_Systolic': 125, 'Cholesterol_Level': 180,
    'Blood_Pressure_Diastolic': 80, 'Cholesterol_Level': 180,
    'Blood_Sugar_Level': 95, 'Sleep_Hours': 7.5,
    'Caloric_Intake': 2200, 'Protein_Intake': 80,
    'Carbohydrate_Intake': 250, 'Fat_Intake': 70
}

prediction = predictor.predict(user_data)
print(f"Calories: {prediction['recommended_calories']} kcal")
print(f"Protein: {prediction['recommended_protein']} g")
```

### **Expected Output Example**
```
🎯 GYMBITE MODEL COMPARISON DEMO
==================================================
📁 Dataset loaded: 5000 records
🤖 Training Enhanced Model
📈 Model Performance:
  Recommended_Calories: R² = 0.968, MAE = 102.5
  Recommended_Protein: R² = 0.960, MAE = 7.6

🔮 ENHANCED PREDICTIONS
🏃‍♀️ Sarah (28F, Active, Weight Loss Goal)
🎯 Complete Nutrition Plan:
  🔥 Calories: 1883 kcal
  🥩 Protein: 84.0 g
  🍞 Carbs: 254.9 g
  🥑 Fats: 75.0 g

🍽️ PERSONALIZED MEAL PLAN
🌅 Breakfast
  📊 Target: 471 kcal | 21.0g protein | 63.7g carbs | 18.8g fats
  💡 Suggestions:
    • Oatmeal with Greek yogurt
    • Eggs with Fruits
    • Smoothie with Greek yogurt
🍽️ Lunch
  📊 Target: 659 kcal | 29.4g protein | 89.2g carbs | 26.2g fats
  💡 Suggestions:
    • Chicken breast with Brown rice
    • Salmon with Quinoa
```

## 🧮 ML Algorithms Explained

### **Random Forest Multi-Output Regression**
- **Algorithm**: Ensemble of 100 decision trees
- **Why chosen**: Handles non-linear relationships, robust to outliers, provides feature importance
- **Multi-output wrapper**: Trains separate trees for each target, maintains correlation

### **Feature Engineering Techniques**
1. **Metabolic Calculations**: BMR (Mifflin-St Jeor), TDEE (activity multipliers)
2. **Risk Scoring**: Composite health assessment using medical thresholds
3. **Categorical Encoding**: Activity levels, health risk categories
4. **Interaction Features**: BMI × Age, Exercise × Steps combinations

### **Validation Strategy**
- **Train/Test Split**: 80/20 with stratification by gender and age groups
- **Cross-validation**: 5-fold CV for hyperparameter tuning
- **Safety bounds**: Post-prediction validation using physiological constraints

---

**🎯 Result**: Professional-grade nutrition ML system with 97% accuracy and built-in safety validation.

Built with scikit-learn, pandas, and domain expertise in nutrition science.
