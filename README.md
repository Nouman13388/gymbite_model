---
title: Gymbite Nutrition Model
emoji: 🥗
colorFrom: orange
colorTo: green
sdk: docker
app_file: app.py
pinned: false
---

# Gymbite - ML Nutrition Recommendation System

Gymbite exposes a small FastAPI service that loads a trained scikit-learn model and serves personalized nutrition recommendations via POST `/predict`.

## 🚀 Live Deployment

**Your app is now deployed on Hugging Face Spaces!**

- **Live URL:** https://huggingface.co/spaces/Nouman1338/gymbite-model
- **Status:** ✅ Active and running
- **Model:** Enhanced Diet Predictor (125.6 MB, Git LFS)
- **Infrastructure:** Python 3.10 + FastAPI + Uvicorn

### Quick Links

- [View Space](https://huggingface.co/spaces/Nouman1338/gymbite-model)
- [Space Settings](https://huggingface.co/spaces/Nouman1338/gymbite-model/settings)
- [Build Logs](https://huggingface.co/spaces/Nouman1338/gymbite-model/logs)
- [GitHub Repository](https://github.com/Nouman13388/gymbite_model)

### Test the Live API

```bash
# Health check
curl https://huggingface.co/spaces/Nouman1338/gymbite-model/health

# Get recommendation
curl -X POST https://huggingface.co/spaces/Nouman1338/gymbite-model/predict \
  -H "Content-Type: application/json" \
  -d '{"Age": 28, "Gender": "Female", "Height_cm": 165.0, "Weight_kg": 75.0, "BMI": 27.5, "Exercise_Frequency": 5, "Daily_Steps": 10000, "Blood_Pressure_Systolic": 125, "Blood_Pressure_Diastolic": 80, "Cholesterol_Level": 180, "Blood_Sugar_Level": 95, "Sleep_Hours": 7.5, "Caloric_Intake": 2200, "Protein_Intake": 80, "Carbohydrate_Intake": 250, "Fat_Intake": 70}'
```

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

## Example requests with curl

Linux/macOS or Windows with curl installed:

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
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
  }'
```

## Example requests with PowerShell

Windows PowerShell:

```powershell
$payload = @{
  Age = 28
  Gender = 'Female'
  Height_cm = 165.0
  Weight_kg = 75.0
  BMI = 27.5
  Exercise_Frequency = 5
  Daily_Steps = 10000
  Blood_Pressure_Systolic = 125
  Blood_Pressure_Diastolic = 80
  Cholesterol_Level = 180
  Blood_Sugar_Level = 95
  Sleep_Hours = 7.5
  Caloric_Intake = 2200
  Protein_Intake = 80
  Carbohydrate_Intake = 250
  Fat_Intake = 70
}
Invoke-RestMethod -Uri http://127.0.0.1:8000/predict `
  -Method Post `
  -Body (ConvertTo-Json $payload) `
  -ContentType 'application/json'
```

## Health / readiness endpoint

GET `/health` returns JSON with these fields:

- `status`: "ok" or "degraded"
- `model_loaded`: boolean
- `uptime_seconds`: float or null

Example healthy response:

```json
{
  "status": "ok",
  "model_loaded": true,
  "uptime_seconds": 123.45
}
```

If the model failed to load at startup, `status` will be `degraded` and `model_loaded` will be `false`. Use this endpoint for readiness probes.

## Docker and Git LFS notes

- The included `Dockerfile` uses `python:3.10-slim` and runs `uvicorn app:app` on port 7860.
- `.dockerignore` may exclude `*.pkl` by default. For local testing, mount the repo into the container so the model file is available at runtime:

```powershell
docker build -t gymbite_model:local .
docker run --rm -p 7860:7860 -v "$PWD:/app" --name gymbite_local gymbite_model:local
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
- If your editor complains about unresolved imports (fastapi/pydantic/uvicorn), install `requirements.txt` into the environment used by the editor.

## Deployment Guide

### Hugging Face Spaces (Recommended - Already Deployed!)

Your app is already deployed to Hugging Face Spaces. To redeploy or deploy to a new Space:

1. Create a new Space at https://huggingface.co/spaces/new
2. Choose Docker as the SDK
3. Clone or link your GitHub repository
4. Hugging Face will automatically build and deploy your Dockerfile

**Advantages:**

- Free tier with GPU support
- Automatic Docker builds on push
- Git LFS support included
- Easy sharing and collaboration

### Local Docker Deployment

```powershell
docker build -t gymbite_model:local .
docker run --rm -p 7860:7860 -v "$PWD:/app" --name gymbite_local gymbite_model:local
```

### Alternative Platforms

- **Render** (https://render.com) - Deploy from GitHub with auto-rebuild
- **Railway** (https://railway.app) - Simple Docker deployment
- **AWS ECS** - Production-grade container orchestration
- **Azure Container Instances** - Managed container service

See `DEPLOYMENT_CHECKLIST.md` for detailed multi-platform deployment guides.

---

If you would like, I can add a small CI check that confirms `/health` returns `status: ok` after the service starts.
