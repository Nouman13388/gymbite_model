# Gymbite - ML Nutrition Recommendation System

Gymbite is a FastAPI-based nutrition recommendation system powered by a trained scikit-learn model. It provides personalized nutrition recommendations based on user health metrics.

**Key Features:**

- 🎯 ML-powered nutrition recommendations
- ⚡ Fast REST API with FastAPI
- 🔄 Easy local development
- 🚀 Cloud-ready (GCP, AWS, Azure, etc.)
- 📊 Uses scikit-learn Random Forest model (16 inputs → 8 outputs)

## 🏗️ Architecture

```text
User Request → FastAPI Endpoint → scikit-learn Model → JSON Response
```

- **Input:** 16 health/lifestyle parameters
- **Output:** 8 nutrition recommendations
- **Model:** Enhanced Diet Predictor (scikit-learn MultiOutputRegressor)
- **Response Time:** < 50ms

## ⚡ Quick Start - Local Development

### Prerequisites

```bash
Python 3.10+
pip
git
```

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Nouman13388/gymbite_model.git
   cd gymbite_model
   ```

2. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Run the API locally:**

   ```bash
   # Option A: Using Python directly
   python app.py

   # Option B: Using uvicorn
   uvicorn app:app --host 127.0.0.1 --port 8000 --reload
   ```

4. **API is now running at:** `http://localhost:8000`
   - Health check: `http://localhost:8000/health`
   - Predictions: `http://localhost:8000/predict`
   - Docs: `http://localhost:8000/docs` (auto-generated Swagger UI)

## ✅ Endpoint Testing Results

"status": "ok",
"model_loaded": true,
"uptime_seconds": 2.34
}

````

**Status:** ✅ PASSED
**Response Code:** 200 OK

### Prediction Endpoint Test Results

**Request:**

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
````

**Response:**

```json
{
  "recommended_calories": 1889,
  "recommended_protein": 84.0,
  "recommended_carbs": 251.9,
  "recommended_fats": 73.9,
  "bmr": 1480,
  "tdee": 2368,
  "health_risk_score": 25,
  "activity_level_score": 6.9
}
```

**Status:** ✅ PASSED
**Response Code:** 200 OK
**Processing Time:** < 100ms

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

## 🐳 Docker & Local Deployment

### Build and Run with Docker

```bash
# Build the Docker image
docker build -t gymbite_model:local .

# Run the container
docker run --rm -p 8000:8000 -v "$PWD:/app" --name gymbite_local gymbite_model:local
```

The API will be available at `http://localhost:8000`

### Git LFS (Large File Storage)

The model file is tracked with Git LFS. To pull it locally:

```bash
# Install Git LFS if not already installed
git lfs install

# Pull LFS files
git lfs pull

# Verify the model file exists
ls -lh enhanced_diet_predictor.pkl
```

## ☁️ Cloud Deployment

### Google Cloud Platform (GCP) - Recommended for Free Tier

Deploy to Google Cloud Run (free tier: 2 million requests/month):

**Current Status:** 🚀 **Live at:** https://gymbite-model-480367101608.europe-west1.run.app

#### Deployment Notes

The application uses **lazy loading** for the ML model:
- The app starts immediately without loading the model
- The model loads on the first prediction request
- This avoids startup timeout issues in Cloud Run

#### Git LFS Model File Handling

The model file (`enhanced_diet_predictor.pkl`, 125.6 MB) is tracked with Git LFS. Cloud Build doesn't automatically pull LFS files, so the app has been configured to:

1. Check if the model file exists locally on startup
2. If missing, download it automatically on the first prediction request
3. Cache it for subsequent requests

This ensures the API works seamlessly both locally and in the cloud.

### Other Cloud Platforms

- **Azure Container Instances** - Pay-per-use Docker containers
- **AWS Lambda** with API Gateway - Serverless option
- **DigitalOcean App Platform** - Simple Docker deployment with free tier
- **Render.com** - Free tier available

### Environment Variables (for Cloud Deployment)

Create a `.env.example` file for reference:

```bash
PORT=8000
HOST=0.0.0.0
LOG_LEVEL=info
```

## 🔧 Troubleshooting

- **Model not found:** Run `git lfs pull` to download the model file from Git LFS
- **Import errors:** Install dependencies with `pip install -r requirements.txt`
- **Port already in use:** Change port with `--port 9000` in uvicorn command

### Alternative Platforms

- **Render** (https://render.com) - Deploy from GitHub with auto-rebuild
- **Railway** (https://railway.app) - Simple Docker deployment
- **AWS ECS** - Production-grade container orchestration
- **Azure Container Instances** - Managed container service

See `DEPLOYMENT_CHECKLIST.md` for detailed multi-platform deployment guides.

---

If you would like, I can add a small CI check that confirms `/health` returns `status: ok` after the service starts.
