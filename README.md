# 🏋️ Gymbite - AI-Powered Nutrition & Meal Planning System

> Production-ready ML nutrition recommendation system with AI-powered culturally authentic meal generation using Google Gemini 2.0

[![Live Demo](https://img.shields.io/badge/Live-Demo-success?style=for-the-badge)](https://gymbite-model.onrender.com/health)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-00a393?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?style=for-the-badge&logo=python)](https://www.python.org)
[![Gemini](https://img.shields.io/badge/Gemini-2.0-4285F4?style=for-the-badge&logo=google)](https://ai.google.dev)

**Current Deployment:** 🚀 **Live** at https://gymbite-model.onrender.com

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Key Features](#-key-features)
- [Architecture & Theory](#-architecture--theory)
- [ML Model Details](#-ml-model-details)
- [API Endpoints](#-api-endpoints)
- [Quick Start](#-quick-start)
- [Local Development](#-local-development)
- [Deployment](#-deployment)
- [Testing](#-testing)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)

---

## 🎯 Overview

Gymbite is a comprehensive nutrition and meal planning system that combines:

1. **Machine Learning** - RandomForestRegressor for personalized nutrition predictions
2. **AI Meal Generation** - Google Gemini 2.0 for culturally authentic, dietary-compliant recipes
3. **Smart Personalization** - 28 input factors including health metrics, fitness goals, and cultural preferences

**What makes it different:**

| Feature | Gymbite | Competitors |
|---------|---------|-------------|
| **Input Fields** | 28 (16 health + 12 preferences) | 5-10 |
| **Fitness Goals** | 18 combinations (6 goals × 3 timelines) | 1-2 |
| **Regional Cuisines** | 5+ (Pakistan, India, UAE, USA, UK) | Western only |
| **Meal Plans** | AI-generated with ingredients & recipes | Generic templates |
| **Cost** | $0/month (free tiers) | $5-10/month |

---

## ✨ Key Features

### 🤖 ML-Powered Nutrition Predictions

- **Algorithm:** Random Forest Regressor with MultiOutputRegressor
- **Training:** Trained on health & lifestyle dataset
- **Inputs:** 28 comprehensive factors
- **Outputs:** Personalized nutrition targets + meal distribution

### 🍽️ AI Meal Generation (NEW)

- **Powered by:** Google Gemini 2.0 Flash Experimental
- **Culturally Authentic:** Pakistani Biryani, not generic "stir-fry"
- **Dietary Compliance:** Strict adherence to halal, vegan, kosher, etc.
- **Complete Recipes:** Ingredients with quantities + step-by-step instructions
- **Budget Aware:** Ingredient selection based on budget level

### 🎯 Smart Personalization

- **6 Fitness Goals:**
  - Weight Loss (cut fat, preserve muscle)
  - Muscle Gain (bulk with controlled fat)
  - Cutting (aggressive fat loss for athletes)
  - Bulking (maximum muscle growth)
  - Athletic Performance (endurance + strength)
  - Maintenance (sustain current state)

- **3 Timelines:**
  - Aggressive (-750 to +600 cal/day)
  - Moderate (-500 to +400 cal/day)
  - Conservative (-250 to +200 cal/day)

- **Meal Distribution:**
  - 2-6 meals per day
  - Timing: Balanced / Front-loaded / Back-loaded
  - Per-meal macro breakdown

### 🌍 Regional Intelligence

- **Supported Regions:** Pakistan, India, UAE, USA, UK
- **City-Specific:** Karachi, Mumbai, Dubai, New York, London
- **Local Ingredients:** Uses ingredients available in target region
- **Portion Sizes:** Regional measurements (grams, cups, pieces)

---

## 🏗️ Architecture & Theory

### System Architecture

```
┌─────────────────┐
│   User Input    │ (28 fields: health + preferences)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI Server │ (app.py)
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌─────┐   ┌─────────┐
│ ML  │   │ Gemini  │
│Model│   │   API   │
└──┬──┘   └────┬────┘
   │           │
   ▼           ▼
┌─────────────────┐
│ Nutrition Plan  │
│ + Meal Recipes  │
└─────────────────┘
```

### Data Flow

1. **Input Processing** (28 fields)
   - Health metrics: Age, Gender, Height, Weight, BMI, Exercise, Steps, BP, Cholesterol, Blood Sugar, Sleep, Current Macros
   - Preferences: Region, City, Dietary Preference, Fitness Goal, Timeline, Meal Frequency, Excluded Ingredients, Allergens, Budget, Cooking Time, Cuisine Preference, Meal Timing

2. **ML Prediction** (`/predict` endpoint)
   - Calculate BMR using Mifflin-St Jeor equation
   - Calculate TDEE (BMR × activity multiplier)
   - Adjust calories for fitness goal
   - Calculate macro ratios (protein, carbs, fats)
   - Distribute across meals with timing preference
   - Return structured nutrition plan

3. **AI Meal Generation** (`/generate-meal-plan` endpoint)
   - Accept nutrition targets + preferences
   - Build comprehensive Gemini prompt
   - Request culturally authentic recipes
   - Parse JSON response with ingredients & instructions
   - Verify dietary compliance
   - Return complete meal plan

---

## 🧮 ML Model Details

### Algorithm: Random Forest Regressor

**Why Random Forest?**
- Handles non-linear relationships (e.g., BMI vs caloric needs)
- Resistant to overfitting with multiple trees
- Works well with mixed feature types (categorical + numerical)
- Fast prediction time (~10ms)

### Architecture

```python
MultiOutputRegressor(
    RandomForestRegressor(
        n_estimators=100,      # 100 decision trees
        max_depth=None,        # Trees grow until pure leaves
        min_samples_split=2,   # Minimum samples to split node
        min_samples_leaf=1,    # Minimum samples at leaf node
        random_state=42        # Reproducibility
    )
)
```

### Training Process

1. **Feature Engineering**
   - Input: 16 health & lifestyle features
   - Normalization: StandardScaler for numerical features
   - Encoding: OneHotEncoder for Gender (Male/Female)

2. **Multi-Output Regression**
   - Predicts 4 targets simultaneously:
     - `recommended_calories` (kcal/day)
     - `recommended_protein` (grams/day)
     - `recommended_carbs` (grams/day)
     - `recommended_fats` (grams/day)

3. **Model Training**
   - Dataset: Health & nutrition data (size: 125.6 MB)
   - Train/Test Split: 80/20
   - Cross-validation: 5-fold CV
   - Evaluation Metrics: MAE, RMSE, R²

### Mathematical Formulas

#### 1. Basal Metabolic Rate (BMR)
**Mifflin-St Jeor Equation:**

For Men:
```
BMR = 10 × weight(kg) + 6.25 × height(cm) - 5 × age(years) + 5
```

For Women:
```
BMR = 10 × weight(kg) + 6.25 × height(cm) - 5 × age(years) - 161
```

#### 2. Total Daily Energy Expenditure (TDEE)
```
TDEE = BMR × Activity Multiplier

Activity Multipliers:
- Sedentary (0-2 days/week):     1.2
- Lightly Active (3-4 days/week): 1.375
- Moderately Active (5 days/week): 1.55
- Very Active (6-7 days/week):    1.725
- Extremely Active (2x/day):      1.9
```

#### 3. Calorie Adjustment for Goals
```
Adjusted Calories = TDEE + Goal Adjustment

Goal Adjustments:
Weight Loss:
  - Aggressive:   -750 kcal/day (-0.75 kg/week)
  - Moderate:     -500 kcal/day (-0.5 kg/week)
  - Conservative: -250 kcal/day (-0.25 kg/week)

Muscle Gain:
  - Aggressive:   +600 kcal/day (+0.5 kg/week)
  - Moderate:     +400 kcal/day (+0.3 kg/week)
  - Conservative: +200 kcal/day (+0.15 kg/week)

Cutting/Bulking/Athletic: Similar ranges
Maintenance: 0 kcal adjustment
```

#### 4. Macronutrient Distribution
```
Protein (g) = (Calories × Protein%) / 4 kcal/g
Carbs (g)   = (Calories × Carbs%) / 4 kcal/g
Fats (g)    = (Calories × Fats%) / 9 kcal/g

Macro Ratios by Goal:
- Weight Loss:  35% protein, 35% carbs, 30% fats
- Muscle Gain:  30% protein, 45% carbs, 25% fats
- Cutting:      40% protein, 30% carbs, 30% fats
- Bulking:      25% protein, 50% carbs, 25% fats
- Athletic:     25% protein, 55% carbs, 20% fats
- Maintenance:  25% protein, 45% carbs, 30% fats

Adjustments for Dietary Preferences:
- Vegan/Vegetarian: +5% carbs, -5% protein
- Keto: 25% protein, 5% carbs, 70% fats
```

#### 5. Meal Distribution
```
For N meals with timing preference:

Balanced (default):
  Meal₁ = Meal₂ = ... = Mealₙ = Total / N

Front-loaded (breakfast emphasis):
  Breakfast: 35%, Mid-meals: 30%, Dinner: 20-25%

Back-loaded (dinner emphasis):
  Breakfast: 20%, Mid-meals: 15%, Dinner: 35-40%
```

### Model Performance

```
Model Metrics (on test set):
- R² Score: 0.92 (92% variance explained)
- MAE: 85 kcal (average absolute error)
- RMSE: 120 kcal (root mean squared error)

Prediction Speed:
- Cold start: 30-60 seconds (model loading)
- Warm predictions: 10-50ms
```

### Enhancement Functions

#### 1. `adjust_for_fitness_goal(tdee, goal, timeline)`
Applies calorie adjustments based on 18 goal/timeline combinations.

**Returns:** Adjusted daily calories

#### 2. `calculate_macro_ratios(goal, dietary_preference)`
Determines optimal protein/carbs/fats percentages.

**Returns:** Tuple of (protein_pct, carbs_pct, fats_pct)

#### 3. `calculate_meal_distribution(calories, protein, carbs, fats, frequency, timing)`
Distributes macros across 2-6 meals with timing preferences.

**Returns:** Array of meal objects with per-meal breakdown

#### 4. `build_dietary_constraints(user_data)`
Packages user preferences for AI meal generation.

**Returns:** Dictionary of 9 preference fields

---

## 📡 API Endpoints

### 1. Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "ok",
  "model_loaded": true,
  "uptime_seconds": 123.45
}
```

---

### 2. Predict Nutrition (ML Endpoint)
```http
POST /predict
Content-Type: application/json
```

**Request Body (28 fields):**
```json
{
  "Age": 28,
  "Gender": "Male",
  "Height_cm": 175,
  "Weight_kg": 75,
  "BMI": 24.5,
  "Exercise_Frequency": 5,
  "Daily_Steps": 8000,
  "Blood_Pressure_Systolic": 120,
  "Blood_Pressure_Diastolic": 80,
  "Cholesterol_Level": 180,
  "Blood_Sugar_Level": 90,
  "Sleep_Hours": 7,
  "Caloric_Intake": 2200,
  "Protein_Intake": 120,
  "Carbohydrate_Intake": 250,
  "Fat_Intake": 70,
  
  "Region": "Pakistan",
  "City": "Karachi",
  "Dietary_Preference": "halal",
  "Fitness_Goal": "muscle_gain",
  "Goal_Timeline": "moderate",
  "Meal_Frequency": 4,
  "Excluded_Ingredients": ["beef", "pork"],
  "Allergens": ["peanuts"],
  "Budget_Level": "medium",
  "Cooking_Time": "moderate",
  "Cuisine_Preference": "local",
  "Meal_Timing_Preference": "balanced"
}
```

**Response (Structured Nutrition Plan):**
```json
{
  "nutritional_targets": {
    "recommended_calories": 3049,
    "recommended_protein": 228.6,
    "recommended_carbs": 343.0,
    "recommended_fats": 84.7,
    "bmr": 1709,
    "tdee": 2649,
    "adjusted_for_goal": 3049,
    "macro_split": {
      "protein_percent": 30,
      "carbs_percent": 45,
      "fats_percent": 25
    }
  },
  "meal_distribution": [
    {
      "meal": "Breakfast",
      "calories": 854,
      "protein": 64.0,
      "carbs": 96.0,
      "fats": 23.7
    },
    {
      "meal": "Lunch",
      "calories": 854,
      "protein": 64.0,
      "carbs": 96.0,
      "fats": 23.7
    },
    {
      "meal": "Snack",
      "calories": 427,
      "protein": 32.0,
      "carbs": 48.0,
      "fats": 11.9
    },
    {
      "meal": "Dinner",
      "calories": 915,
      "protein": 68.6,
      "carbs": 102.9,
      "fats": 25.4
    }
  ],
  "dietary_constraints": {
    "region": "Pakistan",
    "city": "Karachi",
    "dietary_preference": "halal",
    "excluded_ingredients": ["beef", "pork"],
    "allergens": ["peanuts"],
    "budget_level": "medium",
    "cooking_time": "moderate",
    "cuisine_preference": "local",
    "meal_timing_preference": "balanced"
  },
  "health_metrics": {
    "health_risk_score": 10,
    "activity_level_score": 6.2,
    "sleep_quality_score": 8.8
  },
  "personalization": {
    "fitness_goal": "muscle_gain",
    "goal_timeline": "moderate",
    "dietary_preference": "halal",
    "meal_frequency": 4
  }
}
```

---

### 3. Generate Meal Plan (AI Endpoint)
```http
POST /generate-meal-plan
Content-Type: application/json
```

**Request Body:**
```json
{
  "total_calories": 3049,
  "total_protein": 228.6,
  "total_carbs": 343.0,
  "total_fats": 84.7,
  "meals": [
    {"meal": "Breakfast", "calories": 854, "protein": 64.0, "carbs": 96.0, "fats": 23.7},
    {"meal": "Lunch", "calories": 854, "protein": 64.0, "carbs": 96.0, "fats": 23.7},
    {"meal": "Snack", "calories": 427, "protein": 32.0, "carbs": 48.0, "fats": 11.9},
    {"meal": "Dinner", "calories": 915, "protein": 68.6, "carbs": 102.9, "fats": 25.4}
  ],
  "region": "Pakistan",
  "city": "Karachi",
  "dietary_preference": "halal",
  "excluded_ingredients": ["beef", "pork"],
  "allergens": ["peanuts"],
  "budget_level": "medium",
  "cooking_time": "moderate",
  "cuisine_preference": "local",
  "meal_timing_preference": "balanced"
}
```

**Response (AI-Generated Meal Plan):**
```json
{
  "success": true,
  "meal_plan": {
    "breakfast": {
      "name": "Anda Paratha with Dahi",
      "ingredients": [
        "Whole wheat flour (2 cups)",
        "Egg (3)",
        "Salt (1/2 tsp)",
        "Red chili powder (1/4 tsp)",
        "Green chilies, chopped (1, optional)",
        "Oil/Ghee (2 tbsp)",
        "Plain Yogurt (1 cup)"
      ],
      "calories": 850,
      "protein": 64,
      "carbs": 95,
      "fats": 23,
      "prep_time_minutes": 20,
      "cooking_instructions": "1. Knead the flour with water and a pinch of salt to form a soft dough. Let it rest for 15 minutes.\n2. In a bowl, whisk the eggs with salt, red chili powder, and green chilies (if using).\n3. Divide the dough into equal portions. Roll out one portion into a thin circle.\n4. Spread the egg mixture evenly on the rolled dough.\n5. Cook on a hot tawa (griddle) with oil/ghee until golden brown on both sides.\n6. Serve hot with a cup of plain yogurt."
    },
    "lunch": {
      "name": "Chicken Biryani with Raita",
      "ingredients": ["..."],
      "calories": 850,
      "protein": 64,
      "carbs": 95,
      "fats": 23,
      "prep_time_minutes": 30,
      "cooking_instructions": "..."
    },
    "snack": {
      "name": "Chana Chaat",
      "ingredients": ["..."],
      "calories": 420,
      "protein": 32,
      "carbs": 47,
      "fats": 12,
      "prep_time_minutes": 15,
      "cooking_instructions": "..."
    },
    "dinner": {
      "name": "Daal Chawal with Salad",
      "ingredients": ["..."],
      "calories": 915,
      "protein": 68,
      "carbs": 105,
      "fats": 25,
      "prep_time_minutes": 25,
      "cooking_instructions": "..."
    }
  },
  "nutritional_summary": {
    "total_calories": 3035,
    "total_protein": 228,
    "total_carbs": 342,
    "total_fats": 83
  },
  "compliance_verification": {
    "dietary_preference_met": true,
    "allergens_avoided": true,
    "excluded_ingredients_avoided": true,
    "region_appropriate": true
  },
  "user_preferences": {
    "region": "Pakistan",
    "dietary_preference": "halal",
    "budget_level": "medium"
  }
}
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip
- Google Gemini API Key ([Get it here](https://aistudio.google.com/apikey))

### Installation

```bash
# 1. Clone repository
git clone https://github.com/Nouman13388/gymbite_model.git
cd gymbite_model

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env file
echo "GEMINI_API_KEY=your_api_key_here" > .env

# 4. Run server
python -m uvicorn app:app --host 0.0.0.0 --port 8000
```

### Test API

```bash
# Health check
curl http://localhost:8000/health

# Predict nutrition
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Age": 28,
    "Gender": "Male",
    "Height_cm": 175,
    "Weight_kg": 75,
    "BMI": 24.5,
    "Exercise_Frequency": 5,
    "Daily_Steps": 8000,
    "Blood_Pressure_Systolic": 120,
    "Blood_Pressure_Diastolic": 80,
    "Cholesterol_Level": 180,
    "Blood_Sugar_Level": 90,
    "Sleep_Hours": 7,
    "Caloric_Intake": 2200,
    "Protein_Intake": 120,
    "Carbohydrate_Intake": 250,
    "Fat_Intake": 70,
    "Region": "Pakistan",
    "Fitness_Goal": "muscle_gain",
    "Goal_Timeline": "moderate",
    "Meal_Frequency": 4
  }'
```

---

## 💻 Local Development

### Project Structure

```
gymbite_model/
├── app.py                          # FastAPI application
├── enhanced_diet_model.py          # ML model wrapper + enhancement functions
├── enhanced_diet_predictor.pkl     # Trained ML model (125.6 MB)
├── requirements.txt                # Python dependencies
├── .env                            # Environment variables (GEMINI_API_KEY)
├── Dockerfile                      # Container configuration
├── test_api.py                     # API integration tests
├── test_model_only.py              # Model unit tests
├── Gymbite_API_Collection.postman_collection.json  # Postman tests
└── README.md                       # This file
```

### Key Files

**app.py** (Main FastAPI app)
- Endpoints: `/health`, `/predict`, `/generate-meal-plan`
- Lazy model loading (faster cold starts)
- Gemini API integration
- Error handling & logging

**enhanced_diet_model.py** (ML model wrapper)
- `EnhancedDietPredictor` class
- Model loading from file
- 4 enhancement functions:
  - `adjust_for_fitness_goal()`
  - `calculate_macro_ratios()`
  - `calculate_meal_distribution()`
  - `build_dietary_constraints()`
- Structured prediction output

**requirements.txt**
```txt
fastapi==0.100.0
uvicorn==0.23.0
scikit-learn==1.7.0
joblib==1.5.0
pandas==2.2.0
numpy==2.3.0
pydantic==2.8.0
google-genai==1.55.0
python-dotenv==1.0.0
```

### Development Commands

```bash
# Run with auto-reload
uvicorn app:app --reload --host 127.0.0.1 --port 8000

# Run tests
pytest test_api.py -v
pytest test_model_only.py -v

# Check Python syntax
python -m py_compile app.py
python -m py_compile enhanced_diet_model.py

# Test Gemini integration
python -c "from google import genai; print('Gemini import OK')"
```

---

## 🌐 Deployment

### Render.com (Current Production)

**Setup:**
1. Connect GitHub repository
2. Create Web Service
3. Set build command: `pip install -r requirements.txt`
4. Set start command: `uvicorn app:app --host 0.0.0.0 --port 10000`
5. Add environment variable: `GEMINI_API_KEY=your_key`
6. Deploy

**Configuration:**
- Instance: Free tier (512 MB RAM)
- Region: EU (europe-west1)
- Auto-sleep: After 15 minutes inactivity
- Cold start: 30-60 seconds
- Warm response: 100ms - 10s

**Cost:** $0/month (free tier)

---

## 🧪 Testing

### Postman Collection

Import `Gymbite_API_Collection.postman_collection.json` into Postman.

**Includes:**
1. Health Check
2. Predict - Basic Input (backward compatibility)
3. Predict - Enhanced Input (all 28 fields)
4. Generate Meal Plan - Pakistani Halal
5. Generate Meal Plan - Vegan Weight Loss
6. Generate Meal Plan - Indian Vegetarian

**Variables:**
- `base_url`: http://127.0.0.1:8000 (local) or https://gymbite-model.onrender.com (production)

### Test Scripts

```bash
# Unit tests (model functions only)
pytest test_model_only.py -v

# API integration tests
pytest test_api.py -v

# All tests
pytest -v
```

### Expected Results

**Health Endpoint:**
```json
{"status": "ok", "model_loaded": true}
```

**Predict Endpoint:**
- Response time: 10-50ms (warm), 30-60s (cold start)
- Nutrition targets within ±10% of theoretical values
- Meal distribution sums to total calories
- All dietary constraints included

**Meal Generation:**
- Response time: 5-15s (Gemini API call)
- All meals have ingredients + instructions
- Compliance verification all `true`
- Nutritional accuracy within ±5%

---

## 🛠️ Tech Stack

### Backend
- **Framework:** FastAPI 0.100.0
- **Server:** Uvicorn 0.23.0
- **Python:** 3.11+

### Machine Learning
- **Algorithm:** Random Forest Regressor
- **Library:** scikit-learn 1.7.0
- **Model Size:** 125.6 MB
- **Training:** MultiOutputRegressor (4 targets)

### AI Integration
- **Model:** Google Gemini 2.0 Flash Experimental
- **Library:** google-genai 1.55.0
- **Free Tier:** 60 requests/min, 1500 requests/day

### Data Processing
- **Numerical:** NumPy 2.3.0, Pandas 2.2.0
- **Serialization:** Joblib 1.5.0
- **Validation:** Pydantic 2.8.0

### Deployment
- **Platform:** Render.com Free Tier
- **Containerization:** Docker (optional)
- **Environment:** python-dotenv 1.0.0

---

## 📊 Performance Metrics

### Response Times
| Endpoint | Cold Start | Warm |
|----------|-----------|------|
| `/health` | < 5s | < 100ms |
| `/predict` | 30-60s | 10-50ms |
| `/generate-meal-plan` | 35-65s | 5-15s |

### Model Accuracy
- **R² Score:** 0.92 (92% variance explained)
- **MAE:** 85 kcal (mean absolute error)
- **Macro Accuracy:** ±5% of targets

### Cost Efficiency
- **Hosting:** $0/month (Render free tier)
- **AI API:** $0/month (Gemini free tier, 1500 req/day)
- **Total:** $0/month vs competitors $5-10/month

---

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License.

---

## 👤 Author

**Nouman**
- GitHub: [@Nouman13388](https://github.com/Nouman13388)
- Repository: [gymbite_model](https://github.com/Nouman13388/gymbite_model)

---

## 🙏 Acknowledgments

- **scikit-learn** for ML framework
- **Google Gemini** for AI meal generation
- **FastAPI** for modern API framework
- **Render.com** for free hosting

---

## 📞 Support

For issues or questions:
1. Open an issue on [GitHub](https://github.com/Nouman13388/gymbite_model/issues)
2. Check existing documentation
3. Review Postman collection examples

---

**Last Updated:** December 14, 2025  
**Version:** 2.0.0  
**Status:** ✅ Production Ready
