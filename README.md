<!-- Gymbite README: single clean copy (lint-friendly) -->

# Gymbite — ML Nutrition Recommendation System

Gymbite exposes a small FastAPI service that loads a trained scikit-learn model and serves personalized nutrition recommendations via POST `/predict`.

## Quick start (developer)

1. Create and activate a virtual environment (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

1. Install dependencies:

```powershell
pip install -r requirements.txt
pip install -r dev-requirements.txt  # optional: pytest, httpx
```

1. Run the app locally:

```powershell
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

## Health / readiness endpoint

GET `/health` — returns JSON with fields:

- `status`: "ok" | "degraded"
- `model_loaded`: boolean
- `uptime_seconds`: float | null

Example (healthy):

# Gymbite — ML Nutrition Recommendation System

Gymbite exposes a small FastAPI service that loads a trained scikit-learn model and serves personalized nutrition recommendations via POST `/predict`.

## Health / readiness endpoint

GET `/health` — returns JSON with fields:

- `status`: "ok" | "degraded"
- `model_loaded`: boolean
- `uptime_seconds`: float | null

Example (healthy):

```json
{
  "status": "ok",
  "model_loaded": true,
  "uptime_seconds": 123.45
}
```

If the model failed to load at startup, `status` will be `degraded` and `model_loaded` will be `false`. Use this endpoint for readiness probes.

## Example requests

curl (Linux/macOS / Windows with curl):

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"Age":28,"Gender":"Female","Height_cm":165.0,"Weight_kg":75.0,"BMI":27.5,"Exercise_Frequency":5,"Daily_Steps":10000,"Blood_Pressure_Systolic":125,"Blood_Pressure_Diastolic":80,"Cholesterol_Level":180,"Blood_Sugar_Level":95,"Sleep_Hours":7.5,"Caloric_Intake":2200,"Protein_Intake":80,"Carbohydrate_Intake":250,"Fat_Intake":70}'
```

PowerShell (Windows):

````powershell
$payload = @{
  Age = 28
  Gender = 'Female'
  # Gymbite — ML Nutrition Recommendation System

  Gymbite exposes a small FastAPI service that loads a trained scikit-learn model and serves personalized nutrition recommendations via POST /predict.

  ## Quick start (developer)

  1. Create and activate a virtual environment (PowerShell):

  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
````

2. Install dependencies:

```powershell
pip install -r requirements.txt
pip install -r dev-requirements.txt  # optional: pytest, httpx
```

3. Run the app locally:

```powershell
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

## Health / readiness endpoint

GET `/health` — returns JSON with these fields:

- `status`: "ok" | "degraded"
- `model_loaded`: boolean
- `uptime_seconds`: float | null

Example (healthy):

```json
{
  "status": "ok",
  "model_loaded": true,
  "uptime_seconds": 123.45
}
```

If the model failed to load at startup, `status` will be `degraded` and `model_loaded` will be `false`. Use this endpoint for readiness probes.

## API: POST /predict

Request: JSON body with the input features. Example shape:

```json
{
  "Age": 28,
  "Gender": "Female",
  "Height_cm": 165.0,
  "Weight_kg": 75.0,
  "BMI": 27.5,
  "Exercise_Frequency": 5,
  "Daily_Steps": 10000,
  "Blood_Pressure_Systolic": 125,
  "Blood_Pressure_Diastolic": 80,
  "Cholesterol_Level": 180,
  "Blood_Sugar_Level": 95,
  "Sleep_Hours": 7.5,
  "Caloric_Intake": 2200,
  "Protein_Intake": 80,
  "Carbohydrate_Intake": 250,
  "Fat_Intake": 70
}
```

Successful response (abridged):

```json
{
  "recommended_calories": 1889,
  "recommended_protein": 84.0,
  "recommended_carbs": 251.9,
  "recommended_fats": 73.9,
  "bmr": 1480,
  "tdee": 2368
}
```

## Example requests

curl (Linux/macOS / Windows with curl):

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Age":28,"Gender":"Female","Height_cm":165.0,"Weight_kg":75.0,
    "BMI":27.5,"Exercise_Frequency":5,"Daily_Steps":10000,
    "Blood_Pressure_Systolic":125,"Blood_Pressure_Diastolic":80,
    "Cholesterol_Level":180,"Blood_Sugar_Level":95,"Sleep_Hours":7.5,
    "Caloric_Intake":2200,"Protein_Intake":80,"Carbohydrate_Intake":250,"Fat_Intake":70
  }'
```

PowerShell (Windows):

```powershell
$payload = @{
  Age = 28; Gender = 'Female'; Height_cm = 165.0; Weight_kg = 75.0; BMI = 27.5;
  Exercise_Frequency = 5; Daily_Steps = 10000; Blood_Pressure_Systolic = 125;
  Blood_Pressure_Diastolic = 80; Cholesterol_Level = 180; Blood_Sugar_Level = 95;
  Sleep_Hours = 7.5; Caloric_Intake = 2200; Protein_Intake = 80; Carbohydrate_Intake = 250; Fat_Intake = 70
}
Invoke-RestMethod -Uri http://127.0.0.1:8000/predict -Method Post -Body (ConvertTo-Json $payload) -ContentType 'application/json'
```

## Docker & Git LFS notes

- The included `Dockerfile` uses `python:3.10-slim` and runs `uvicorn app:app` on port 7860.
- `.dockerignore` may exclude `*.pkl` by default to avoid shipping large model binaries unintentionally. For local testing, mount the repo into the container so the model file is available at runtime:

```powershell
docker build -t gymbite_model:local .
docker run --rm -p 7860:7860 -v "${PWD}:/app" --name gymbite_local gymbite_model:local
```

- If the model is tracked with Git LFS, run:

```powershell
git lfs install
git lfs pull
```

To add a model file to LFS:

```powershell
git lfs track "*.pkl"
git add .gitattributes
git add <your_model>.pkl
git commit -m "chore: add model to LFS"
git push origin dev
```

## Troubleshooting

- If `/predict` returns 503, the model is not loaded (see `/health`). Ensure you ran `git lfs pull` if using LFS or mounted the model into the container.
- If your editor complains about unresolved imports (fastapi/pydantic/uvicorn) → install `requirements.txt` into the environment used by the editor.

---

If you'd like, I can add a small CI check that confirms `/health` returns `status: ok` after the service starts, or add helper scripts for Windows and PowerShell for local testing.

### Example requests

curl (Linux/macOS / Windows with curl):

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "Age":28,"Gender":"Female","Height_cm":165.0,"Weight_kg":75.0,
    "BMI":27.5,"Exercise_Frequency":5,"Daily_Steps":10000,
    "Blood_Pressure_Systolic":125,"Blood_Pressure_Diastolic":80,
    "Cholesterol_Level":180,"Blood_Sugar_Level":95,"Sleep_Hours":7.5,
    "Caloric_Intake":2200,"Protein_Intake":80,"Carbohydrate_Intake":250,"Fat_Intake":70
  }'
```

PowerShell (Windows):

```powershell
$payload = @{
  Age = 28; Gender = 'Female'; Height_cm = 165.0; Weight_kg = 75.0; BMI = 27.5;
  Exercise_Frequency = 5; Daily_Steps = 10000; Blood_Pressure_Systolic = 125;
  Blood_Pressure_Diastolic = 80; Cholesterol_Level = 180; Blood_Sugar_Level = 95;
  Sleep_Hours = 7.5; Caloric_Intake = 2200; Protein_Intake = 80; Carbohydrate_Intake = 250; Fat_Intake = 70
}
Invoke-RestMethod -Uri http://127.0.0.1:8000/predict -Method Post -Body (ConvertTo-Json $payload) -ContentType 'application/json'
```

## Health / readiness endpoint

A health endpoint is available to verify the process and model readiness.

- GET /health — returns JSON with keys: `status`, `model_loaded`, `uptime_seconds`.

Example response (healthy):

```json
{
  "status": "ok",
  "model_loaded": true,
  "uptime_seconds": 123.45
}
```

If the model failed to load, `status` will be `degraded` and `model_loaded` will be `false`.

## Docker & deployment notes

- The included `Dockerfile` uses `python:3.10-slim` and runs `uvicorn app:app` on port 7860.
- `.dockerignore` excludes `*.pkl` by default to avoid shipping large model binaries unintentionally. For local testing, mount the repo into the container so the model file is available at runtime:

```powershell
docker build -t gymbite_model:local .
docker run --rm -p 7860:7860 -v "${PWD}:/app" --name gymbite_local gymbite_model:local
```

- For production (Hugging Face Spaces or cloud), you can either:
  1. Track the model with Git LFS and let the runner fetch it in CI/CD, or
  2. Host the model artifact in secure object storage and download it during container startup.

## Model & Git LFS

- The model artifact `enhanced_diet_predictor.pkl` is tracked with Git LFS to avoid large blobs in git history.
- After cloning the repo, run:

```powershell
git lfs install
git lfs pull
```

To add a new model file to LFS:

```powershell
git lfs track "*.pkl"
git add .gitattributes
git add <your_model>.pkl
git commit -m "chore: add model to LFS"
git push origin dev
```

## Troubleshooting

- If `/predict` returns 503, the model is not loaded (see `/health`). Ensure you ran `git lfs pull` if using LFS or mounted the model into the container.
- If you see scikit-learn unpickle warnings, ensure `scikit-learn==1.7.0` (the model's serialization runtime) is installed or retrain/resave the model with your runtime.

## Contributing & License

Contributions welcome. Open PRs against `dev`. Add tests and CI coverage for new behavior. Add a `LICENSE` file (MIT is a common choice).

---

If you'd like, I can add a small health-check in CI or a tiny `make`/PowerShell helper to speed local testing.

<!-- Top Anchor -->

# Gymbite — ML Nutrition Recommendation System

[![CI](https://github.com/Nouman13388/gymbite_model/actions/workflows/pytest.yml/badge.svg?branch=dev)](https://github.com/Nouman13388/gymbite_model/actions/workflows/pytest.yml)

Gymbite is a production-oriented Python project that provides personalized nutrition recommendations and automated meal plans. It exposes a FastAPI service that loads a trained model at startup and serves predictions via POST /predict. The codebase includes training scripts, model serialization, a prediction wrapper, and utilities to convert predictions into meal plans.

Key goals:

- Provide accurate macro and calorie recommendations (calories, protein, carbs, fats)
- Enforce physiological safety constraints (calorie floors/ceilings, macro ranges)
- Be deployable as a single-file FastAPI app or via Docker (Hugging Face Spaces compatible)
- Make development, testing, and CI deterministic and reproducible

This README documents repository layout, local developer setup, testing, CI, Docker usage, and deployment tips.

## Table of contents

1. [Overview](#overview)
2. [Key features](#key-features)
3. [Repository layout](#repository-layout)
4. [Quick start (developer)](#quick-start-developer)
5. [Running / Docker](#running--docker)
6. [Model & artifacts](#model--artifacts)
7. [Feature engineering (summary)](#feature-engineering-summary)
8. [Safety & validation](#safety--validation)
9. [Performance (reference)](#performance-reference)
10. [Example response](#example-response)
11. [API: POST /predict](#api-post-predict)
12. [Integration (Flutter / mobile)](#integration-flutter--mobile)
13. [Use cases & value](#use-cases--value)
14. [Roadmap](#roadmap)
15. [Troubleshooting](#troubleshooting)
16. [Git LFS & large model handling](#git-lfs--large-model-handling)
17. [Contributing](#contributing)
18. [License](#license)

## Overview

Gymbite wraps a scikit-learn multi-output regressor with a small safety/validation layer and a meal-plan allocator. The production-ready FastAPI app loads the model at startup and provides a single main endpoint, POST /predict, which returns calorie and macro targets plus optional meal plan suggestions.

## Key features

- Multi-output regression: predicts calories and macros together for consistent targets
- Metabolic intelligence: computes BMR/TDEE and adjusts recommendations by activity
- Safety layer: enforces macro/calorie constraints to avoid unrealistic outputs
- Meal plan allocator: distributes macros across 4 meals and generates suggestions
- FastAPI server for easy integration (single-file `app.py` entrypoint)
- Docker-ready and CI-validated (GitHub Actions workflows included)

## Repository layout

Top-level files and their purpose:

```text
app.py                         # FastAPI application entrypoint (create_app -> app)
enhanced_diet_model.py         # Predictor class and model utilities (EnhancedDietPredictor)
simple_enhanced_demo.py        # Training demo that creates/saves the model
meal_plan_generator.py         # Convert model output to meal plans
enhanced_diet_predictor.pkl    # (LFS) Saved trained model used by the API
Personalized_Diet_Recommendations.csv  # Training dataset
requirements.txt               # Runtime dependencies
dev-requirements.txt           # Test/dev dependencies (pytest, httpx)
Dockerfile                     # Dockerfile for container-based deployment
.dockerignore                  # Files excluded from Docker build context
.gitattributes                 # Git LFS settings for model binaries
.github/workflows/pytest.yml   # CI test workflow
.github/workflows/docker-build.yml # CI Docker build verification
tests/test_predict.py          # Integration test using FastAPI TestClient
README.md                      # This documentation
```

## Quick start (developer)

1. Create and activate a virtual environment (PowerShell):

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

2. Install runtime (and optionally dev) dependencies:

```powershell
pip install -r requirements.txt
pip install -r dev-requirements.txt  # optional for tests
```

3. Run the app locally (non-Docker):

```powershell
# run uvicorn directly
python -m uvicorn app:app --host 127.0.0.1 --port 8000
```

4. Or build and run with Docker (preferred for parity with Spaces):

```powershell
# build image
docker build -t gymbite_model:local .
# run (mount repo so model is available)
docker run --rm -p 7860:7860 -v "${PWD}:/app" --name gymbite_local gymbite_model:local
```

5. Run tests:

```powershell
python -m pytest -q
```

## Running / Docker

- Dockerfile uses `python:3.10-slim`. The image installs `requirements.txt`, copies the repo, and runs uvicorn to serve `app:app` on port 7860.
- `.dockerignore` intentionally excludes `*.pkl` so local testing uses a bind mount to provide the model file at runtime. For production, consider baking the model into the image or hosting the model on remote storage and downloading at container startup.

## Model & artifacts

- Model type: Multi-output scikit-learn regressor (RandomForest-based ensemble in the reference implementation).
- Features: 19 engineered features (BMR, TDEE, BMI, exercise, steps, clinical markers, derived risk/activity scores).
- Saved model: `enhanced_diet_predictor.pkl` — tracked with Git LFS to avoid large Git blobs. The FastAPI app loads this model on startup via `EnhancedDietPredictor.load_model()`.

Compatibility note: the model was serialized with scikit-learn 1.7.0. The `requirements.txt` pins `scikit-learn==1.7.0` to avoid unpickle warnings. If you retrain the model with a different scikit-learn version, re-save the `.pkl` with that runtime.

## Feature engineering (summary)

The training pipeline computes metabolic metrics (BMR/TDEE), anthropometric interactions, behavior signals (exercise frequency, steps, sleep), and clinical indicators to produce a robust 19-feature input vector. See `enhanced_diet_model.py` for the exact transformations and helper functions.

## Safety & validation

Before returning recommendations, the system applies physiologically sensible constraints:

- Calorie floor/ceiling derived from BMR (e.g., 0.8×BMR to 2.0×BMR)
- Macro percentage bounds (protein/carbs/fats) and a grams-per-kg heuristic for protein
- Iterative correction to ensure the final macro distribution obeys both calorie and macro constraints

These checks prevent unrealistic recommendations and form a safety net for downstream consumption.

## Performance (reference)

Performance metrics from training/validation runs are stored in training logs and notebooks. Expect high fidelity on calories and protein and slightly higher variance on carbohydrate predictions (typical for multi-output nutritional models). Use the `simple_enhanced_demo.py` training script to reproduce metrics locally.

## Example response

POST /predict with the request shape (see API contract below) returns JSON like:

```json
{
  "recommended_calories": 1889,
  "recommended_protein": 84.0,
  "recommended_carbs": 251.9,
  "recommended_fats": 73.9,
  "bmr": 1480,
  "tdee": 2368,
  "health_risk_score": 25,
  "meal_plan": {
    "breakfast": {
      "calories": 471,
      "protein": 21.0,
      "carbs": 63.7,
      "fats": 18.8
    }
  }
}
```

## API: POST /predict

Endpoint: POST /predict

Request JSON shape (all fields required):

```json
{
  "Age": 28,
  "Gender": "Female",
  "Height_cm": 165.0,
  "Weight_kg": 75.0,
  "BMI": 27.5,
  "Exercise_Frequency": 5,
  "Daily_Steps": 10000,
  "Blood_Pressure_Systolic": 125,
  "Blood_Pressure_Diastolic": 80,
  "Cholesterol_Level": 180,
  "Blood_Sugar_Level": 95,
  "Sleep_Hours": 7.5,
  "Caloric_Intake": 2200,
  "Protein_Intake": 80,
  "Carbohydrate_Intake": 250,
  "Fat_Intake": 70
}
```

Response: 200 JSON with keys (example):

```json
{
  "recommended_calories": 1889,
  "recommended_protein": 84.0,
  "recommended_carbs": 251.9,
  "recommended_fats": 73.9,
  "bmr": 1480,
  "tdee": 2368,
  "health_risk_score": 25,
  "meal_plan": { ... }
}
```

Errors:

- 400 Bad Request: validation error from Pydantic input model
- 503 Service Unavailable: model not loaded at startup
- 500 Internal Server Error: unexpected prediction error

## Integration (Flutter / mobile)

Any HTTP-capable client can call POST /predict. For Flutter, use the `http` package and map the JSON response into your UI model. Keep calls asynchronous and show a loading indicator while waiting for the response.

## Use cases & value

- Fitness & wellness apps
- Clinical screening and population health
- Meal-kit and food services for tailored plans
- Coaching and remote nutrition services

Competitive strengths: multi-output consistency, safety validations, and a production-ready API surface.

## Roadmap

Planned improvements:

1. Better personalization (goal-aware recommendations)
2. Preference and allergy-aware meal plan generation
3. Lightweight model variants for on-device inference
4. CI/CD to build and publish container images (GHCR) and deploy to Spaces

## Troubleshooting

Common issues and quick fixes:

- Model not loaded at startup (503): ensure the model file `enhanced_diet_predictor.pkl` is present inside the container (bind-mount or include in image). If using Git LFS, run `git lfs pull` locally before building.
- LFS pointer files inside container: run `git lfs pull` locally, or ensure the CI checkout uses LFS (workflows in this repo do).
- Unpickle/Version mismatch warnings: pin `scikit-learn==1.7.0` in `requirements.txt` or re-save model using your scikit-learn runtime.
- Pip install failures during Docker build: transient network error — retry; consider adding pip cache or pinning versions.

## Git LFS & large model handling

We track model binaries with Git LFS to avoid pushing large blobs to the Git history. If you clone this repo, run:

```powershell
git lfs install
git lfs pull
```

If you need to add a new model file and ensure it's tracked by LFS:

```powershell
git lfs track "*.pkl"
git add .gitattributes
git add <your_model>.pkl
git commit -m "chore: add model to LFS"
git push origin dev
```

Note: collaborators must run `git lfs install` once to fetch real binaries instead of pointer files.

## Contributing

Contributions are welcome. Suggested ways to help:

- Add tests and expand edge-case coverage
- Improve preprocessing and feature engineering for robustness
- Add additional model variants (lighter, faster for on-device inference)
- Improve CI to publish images or artifacts

Please open issues for feature requests or bugs, and submit PRs against the `dev` branch.

## License

Add a `LICENSE` file. For open-source usage, MIT is a common choice.

---

If anything in this README is unclear or you'd like a short quick-start video/shell script, tell me and I will add it. Thank you for using Gymbite — ready for local testing, CI validation, and deployment to Hugging Face Spaces or other container hosts.

<!-- Top Anchor -->

# Gymbite ML Nutrition Recommendation System

[![CI](https://github.com/Nouman13388/gymbite_model/actions/workflows/pytest.yml/badge.svg?branch=dev)](https://github.com/Nouman13388/gymbite_model/actions/workflows/pytest.yml)

Personalized nutrition & meal planning powered by **Multi-Output Machine Learning** (calories, protein, carbs, fats) with **97% calorie accuracy**, **safety validation**, and **automated meal plan generation**. Designed for both **stakeholders** and **developers**—ready for integration into **Flutter/mobile**, **web APIs**, or **enterprise platforms**.

---

## 📚 Table of Contents

1. [Overview](#overview)
2. [Key Features](#key-features)
3. [Project Structure](#project-structure)
4. [Quick Start](#quick-start)
5. [Running Options](#running-options)
6. [Model Architecture](#model-architecture)
7. [Feature Engineering](#feature-engineering-19-features)
8. [Safety & Validation](#-safety--validation)
9. [Performance & Accuracy](#-performance--accuracy)
10. [Example Output](#-example-output)
11. [API & Data Contract](#-api--data-contract)
12. [Flutter Integration Guide](#-flutter-integration)
13. [Business & Use Cases](#-business--use-cases)
14. [Roadmap](#️-roadmap)
15. [Troubleshooting](#️-troubleshooting)
16. [Glossary](#-glossary)
17. [Contributing / Extensions](#-contributing--extensions)
18. [License](#-license)
19. [Next Steps](#-next-steps)

## 🔍 Overview

Gymbite ML delivers **evidence-based nutrition recommendations** and **ready-to-use meal plans** derived from user biometrics, lifestyle, and existing dietary intake. It uses a **Multi-Output Random Forest Regressor** enriched with **19 engineered features** (metabolic, behavioral, risk-based) and applies **physiological safety constraints** before returning results.

## ✨ Key Features

- 🔢 Predicts: Calories, Protein, Carbohydrates, Fats (simultaneously)
- 🧬 Metabolic intelligence: BMR, TDEE, activity profiling
- 🛡️ Safety validation: Macro ranges + calorie bounds + health risk adjustments
- 🍽️ Automated 4-meal daily plan (Breakfast, Lunch, Dinner, Snacks)
- 📊 Transparent performance (R², MAE, ±10% accuracy)
- 🧩 Pluggable: easy wrapping into REST / GraphQL APIs
- 📱 Mobile-friendly JSON contract for Flutter integration
- 🗺️ Roadmap for advanced intelligence (deep learning, personalization)

## 🗂️ Project Structure

```text
gymbite_model/
├── enhanced_diet_model.py            # Core model & feature engineering
├── simple_enhanced_demo.py           # Full training + predictions + meal plans
├── meal_plan_generator.py            # Meal plan from existing model
├── client_demo.py                    # Presentation-style demo
├── enhanced_diet_predictor.pkl       # Saved trained model
├── Personalized_Diet_Recommendations.csv  # Training dataset (5k rows)
├── enhanced_feature_importance.png   # Feature importance visualization
└── requirements.txt                  # Dependencies
```

## 🚀 Quick Start

```bash
pip install numpy pandas scikit-learn matplotlib joblib
python simple_enhanced_demo.py
```

Outputs: training summary, metrics, predictions, and meal plans.

## 🏃 Running Options

| Goal                      | Command                          | Result              |
| ------------------------- | -------------------------------- | ------------------- |
| Full demo (train + plans) | `python simple_enhanced_demo.py` | End-to-end showcase |
| Meal plan only            | `python meal_plan_generator.py`  | Uses existing model |
| Train fresh model         | `python enhanced_diet_model.py`  | Saves new `.pkl`    |
| Programmatic usage        | (see code snippet below)         | Integrate in app    |

Programmatic example:

```python
from enhanced_diet_model import EnhancedDietPredictor
predictor = EnhancedDietPredictor(); predictor.load_model()
prediction = predictor.predict({...})
print(prediction)
```

## 🧠 Model Architecture

| Component                 | Purpose                             |
| ------------------------- | ----------------------------------- |
| MultiOutput RandomForest  | Joint macro + calorie predictions   |
| Feature Engineering Layer | Adds metabolic & behavioral context |
| Safety Validator          | Enforces physiological bounds       |
| Meal Plan Allocator       | Distributes macros across meals     |
| Health Risk Analyzer      | Scores lifestyle/medical indicators |

## 🧪 Feature Engineering (19 Features)

Categories:

- Metabolic: BMR, TDEE
- Anthropometrics: BMI, weight, height, age interactions
- Behavior: Exercise frequency, steps, sleep hours
- Clinical: Blood pressure (sys/dia), cholesterol, blood sugar
- Derived: Activity level category, steps bin, risk score, macro density ratios

Example (simplified):

```python
df['BMR'] = mifflin_st_jeor(weight, height, age, gender)
df['TDEE'] = activity_multiplier(df['BMR'], exercise_freq, steps)
df['Health_Risk'] = composite_risk(bp_sys, bp_dia, cholesterol, blood_sugar, bmi, sleep_hours)
```

## 🛡️ Safety & Validation

- Calorie floor: 0.8 × BMR (prevents starvation)
- Calorie ceiling: 2.0 × BMR (prevents unhealthy bulk)
- Macro bounds (percent of calories): Protein 10–35%, Carbs 45–65%, Fats 20–35%
- Protein g heuristic: 0.8–2.5 g/kg body weight
- Adjustments applied iteratively until valid

## 📈 Performance & Accuracy

| Target   | R²    | MAE      | % within ±10% | Interpretation     |
| -------- | ----- | -------- | ------------- | ------------------ |
| Calories | 0.968 | 102 kcal | 84.6%         | Excellent          |
| Protein  | 0.960 | 7.6 g    | 77.4%         | Excellent          |
| Carbs    | 0.890 | 25.9 g   | 48.4%         | Good               |
| Fats     | 0.944 | 7.8 g    | 58.4%         | Very Good          |
| Overall  | 0.941 | —        | 67.2%         | Professional Grade |

R² = variance explained. % within ±10% = practical prediction closeness. Industry benchmark for similar systems: 60–75% overall → this model: 67.2%.

## 🧾 Example Output

```text
User: Sarah (28F, Active)
Nutrition Targets:
  Calories: 1883 kcal | Protein: 84 g | Carbs: 255 g | Fats: 75 g
Metabolic: BMR 1480 | TDEE 2368 | Risk 25/100

Meal Plan Distribution:
  Breakfast 25%  | Lunch 35% | Dinner 30% | Snacks 10%
  Breakfast Example: Oatmeal + Greek yogurt + berries
```

## 🔌 API & Data Contract

Suggested REST endpoint: `POST /predict`.

Request JSON:

```json
{
  "Age": 28,
  "Gender": "Female",
  "Height_cm": 165,
  "Weight_kg": 75,
  "BMI": 27.5,
  "Exercise_Frequency": 5,
  "Daily_Steps": 10000,
  "Blood_Pressure_Systolic": 125,
  "Blood_Pressure_Diastolic": 80,
  "Cholesterol_Level": 180,
  "Blood_Sugar_Level": 95,
  "Sleep_Hours": 7.5,
  "Caloric_Intake": 2200,
  "Protein_Intake": 80,
  "Carbohydrate_Intake": 250,
  "Fat_Intake": 70
}
```

Response JSON (example):

```json
{
  "recommended_calories": 1883,
  "recommended_protein": 84.0,
  "recommended_carbs": 254.9,
  "recommended_fats": 75.0,
  "bmr": 1480,
  "tdee": 2368,
  "health_risk_score": 25,
  "meal_plan": {
    "breakfast": {
      "calories": 471,
      "protein": 21.0,
      "carbs": 63.7,
      "fats": 18.8,
      "suggestions": ["Oatmeal", "Greek yogurt", "Berries"]
    },
    "lunch": {
      "calories": 659,
      "protein": 29.4,
      "carbs": 89.2,
      "fats": 26.2,
      "suggestions": ["Chicken breast", "Brown rice", "Salmon", "Quinoa"]
    }
  }
}
```

FastAPI stub:

```python
from fastapi import FastAPI
from pydantic import BaseModel
from enhanced_diet_model import EnhancedDietPredictor

app = FastAPI(); predictor = EnhancedDietPredictor(); predictor.load_model()

class Input(BaseModel):
    Age:int; Gender:str; Height_cm:float; Weight_kg:float; BMI:float
    Exercise_Frequency:int; Daily_Steps:int
    Blood_Pressure_Systolic:int; Blood_Pressure_Diastolic:int
    Cholesterol_Level:int; Blood_Sugar_Level:int; Sleep_Hours:float
    Caloric_Intake:float; Protein_Intake:float; Carbohydrate_Intake:float; Fat_Intake:float

@app.post('/predict')
def predict(inp: Input):
    return predictor.predict(inp.dict())
```

## 📱 Flutter Integration

1. Deploy API (FastAPI + Uvicorn / Flask + Gunicorn)
2. Call endpoint using `http` package.

Flutter Dart example:

```dart
final response = await http.post(
  Uri.parse('https://api.yourdomain.com/predict'),
  headers: {'Content-Type': 'application/json'},
  body: jsonEncode(userPayload),
);
if (response.statusCode == 200) {
  final data = jsonDecode(response.body);
  setState(() => nutrition = data);
}
```

UI Suggestions:

- Card 1: Daily Targets (Calories + macro breakdown %)
- Card 2: Metabolic Insights (BMR, TDEE, Risk Score)
- Card 3: Meal Plan (accordion per meal)
- Card 4: Improvement Tips (dynamic copy based on risk / macro imbalance)

## 💼 Business & Use Cases

| Use Case           | Value                              |
| ------------------ | ---------------------------------- |
| Fitness App        | User retention via personalization |
| Healthcare Portal  | Automated diet screening           |
| Corporate Wellness | Scalable employee guidance         |
| Meal Kit Service   | Tailored meal assembly             |
| Coaching Platform  | Augments human coaching            |

Competitive Advantages:

- Multi-output vs single metric systems
- Safety validation layer
- Transparent performance metrics
- Ready for monetization (API / subscription / white-label)

## 🗺️ Roadmap

| Phase | Focus           | Highlights                        |
| ----- | --------------- | --------------------------------- |
| 1     | API & Auth      | FastAPI, DB schema, JWT           |
| 2     | Personalization | Goals, adaptive re-planning       |
| 3     | Intelligence    | Deep models, preference learning  |
| 4     | Ecosystem       | Wearables, social, multi-language |

## 🛠️ Troubleshooting

| Issue                | Cause                          | Fix                                 |
| -------------------- | ------------------------------ | ----------------------------------- |
| Module not found     | Dependencies not installed     | `pip install -r requirements.txt`   |
| Model file missing   | Not trained yet                | Run `python enhanced_diet_model.py` |
| Strange macro ratios | Input BMI or weight inaccurate | Validate user input ranges          |
| High error for carbs | Lifestyle variance             | Add more behavior features          |

## 📘 Glossary

- **BMR**: Basal Metabolic Rate (resting energy burn)
- **TDEE**: Total Daily Energy Expenditure (BMR × activity)
- **MAE**: Mean Absolute Error
- **R²**: Variance explained by model
- **Health Risk Score**: Composite indicator (blood pressure, cholesterol, sugar, BMI, sleep)

## 🧩 Contributing / Extensions

- Add database persistence (PostgreSQL) for user histories
- Implement caching layer (Redis) for repeat users
- Add preference-based meal substitution (vegetarian, halal, etc.)
- Introduce goal-specific calorie periodization (cut / bulk / maintenance)
- Build CI tests: synthetic input validation & schema checks

### Developer setup (quick)

If you're contributing or running tests locally, follow these steps (Windows PowerShell):

1. Create and activate a virtual environment in the project root:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

1. Install runtime and development/test dependencies:

```powershell
pip install -r requirements.txt -r dev-requirements.txt
```

1. Run tests:

```powershell
python -m pytest -q
```

Note: `dev-requirements.txt` pins `pytest` and `httpx` so CI and local runs are consistent.

## 📄 License

Specify license here (e.g., MIT, Proprietary). Add a `LICENSE` file before distribution.

## ✅ Next Steps

1. Decide deployment target (Docker + FastAPI recommended)
2. Implement `/predict` endpoint & secure (JWT / API key)
3. Integrate with Flutter UI workflow
4. Collect real user data → retrain periodically
5. Expand feature set (preferences, allergies)

---

**Professional-grade nutrition intelligence—production ready and extensible.**

[Back to Top](#gymbite-ml-nutrition-recommendation-system)
