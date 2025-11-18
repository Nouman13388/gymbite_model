# Gymbite - ML Nutrition Recommendation System# Gymbite - ML Nutrition Recommendation System# Gymbite - ML Nutrition Recommendation System

> A production-ready FastAPI-based nutrition recommendation system powered by scikit-learn ML model. Get personalized nutrition guidance based on comprehensive health metrics.

**Current Deployment Status:** 🚀 **Live** at https://gymbite-model-480367101608.europe-west1.run.app> A production-ready FastAPI-based nutrition recommendation system powered by scikit-learn ML model. Get personalized nutrition guidance based on comprehensive health metrics.Gymbite is a FastAPI-based nutrition recommendation system powered by a trained scikit-learn model. It provides personalized nutrition recommendations based on user health metrics.

---

## 📋 Table of Contents**Current Deployment Status:** 🚀 **Live** at https://gymbite-model-480367101608.europe-west1.run.app**Key Features:\*\*

- [Features](#-features)

- [Quick Start](#-quick-start)

- [Architecture](#-architecture)---- 🎯 ML-powered nutrition recommendations

- [API Endpoints](#-api-endpoints)

- [Testing](#-testing)- ⚡ Fast REST API with FastAPI

- [Cloud Deployment](#-cloud-deployment)

- [Local Development](#-local-development)## 📋 Table of Contents- 🔄 Easy local development

- [Troubleshooting](#-troubleshooting)

- 🚀 Cloud-ready (GCP, AWS, Azure, etc.)

---

- [Features](#-features)- 📊 Uses scikit-learn Random Forest model (16 inputs → 8 outputs)

## 🎯 Features

- [Quick Start](#-quick-start)

- ✅ **ML-Powered Predictions** - scikit-learn Random Forest with 16 inputs → 8 outputs

- ⚡ **Fast API** - Sub-100ms response time with FastAPI framework- [Architecture](#-architecture)## 🏗️ Architecture

- 🔄 **Lazy Model Loading** - App starts instantly, model loads on first request

- 📊 **8 Recommendation Outputs** - Calories, protein, carbs, fats, BMR, TDEE, health risk score, activity level- [API Endpoints](#-api-endpoints)

- 🐳 **Docker Ready** - Containerized for GCP Cloud Run and other platforms

- 🧪 **Fully Tested** - 5 pytest test cases with 100% pass rate- [Testing](#-testing)```text

- 📡 **GitHub Releases** - Automatic model download from GitHub releases (solves Git LFS issue)

- 🌐 **Production Ready** - Health checks, error handling, input validation- [Cloud Deployment](#-cloud-deployment)User Request → FastAPI Endpoint → scikit-learn Model → JSON Response

---- [Local Development](#-local-development)```

## ⚡ Quick Start- [Troubleshooting](#-troubleshooting)

### 30-Second Local Setup- [Project Structure](#-project-structure)- **Input:** 16 health/lifestyle parameters

```bash- **Output:** 8 nutrition recommendations

# 1. Clone and navigate

git clone https://github.com/Nouman13388/gymbite_model.git---- **Model:** Enhanced Diet Predictor (scikit-learn MultiOutputRegressor)

cd gymbite_model

- **Response Time:** < 50ms

# 2. Create virtual environment

python -m venv .venv## 🎯 Features

.\.venv\Scripts\Activate.ps1  # Windows PowerShell

# or: source .venv/bin/activate  # macOS/Linux## ⚡ Quick Start - Local Development



# 3. Install and run- ✅ **ML-Powered Predictions** - scikit-learn Random Forest with 16 inputs → 8 outputs

pip install -r requirements.txt

python app.py- ⚡ **Fast API** - Sub-100ms response time with FastAPI framework### Prerequisites

```

- 🔄 **Lazy Model Loading** - App starts instantly, model loads on first request

**API will be available at:** `http://localhost:8000`

- 📊 **8 Recommendation Outputs** - Calories, protein, carbs, fats, BMR, TDEE, health risk score, activity level```bash

### 🔗 Useful Links

- 🐳 **Docker Ready** - Containerized for GCP Cloud Run and other platformsPython 3.10+

- **Swagger UI (Interactive Docs):** http://localhost:8000/docs

- **ReDoc (Alternative Docs):** http://localhost:8000/redoc- 🧪 **Fully Tested** - 5 pytest test cases with 100% pass ratepip

- **Health Check:** http://localhost:8000/health

- **Predictions:** http://localhost:8000/predict (POST)- 📡 **GitHub Releases** - Automatic model download from GitHub releases (solves Git LFS issue)git

---- 🌐 **Production Ready** - Health checks, error handling, input validation```

## 🏗️ Architecture

`````---### Installation

┌─────────────────┐

│   User Request  │

├─────────────────┤

│  FastAPI Router │## ⚡ Quick Start1. **Clone the repository:**

├─────────────────┤

│ Input Validation│ (Pydantic)

├─────────────────┤

│  Load Model*    │ (*lazy load on first request)### 30-Second Local Setup   ```bash

├─────────────────┤

│  Make Prediction│ (scikit-learn)   git clone https://github.com/Nouman13388/gymbite_model.git

├─────────────────┤

│ Validate Output │ (Health-safe bounds)```bash   cd gymbite_model

├─────────────────┤

│  JSON Response  │# 1. Clone and navigate   ```

└─────────────────┘

```git clone https://github.com/Nouman13388/gymbite_model.git



### Key Componentscd gymbite_model2. **Install dependencies:**



| Component | Details |

|-----------|---------|

| **Framework** | FastAPI 0.104+ with Uvicorn |# 2. Create virtual environment   ```bash

| **ML Model** | scikit-learn MultiOutputRegressor (Random Forest) |

| **Model Size** | 125.6 MB (tracked via Git LFS, auto-downloaded) |python -m venv .venv   pip install -r requirements.txt

| **Python Version** | 3.10+ |

| **Deployment** | Google Cloud Run (2 GB memory, 600s timeout) |.\.venv\Scripts\Activate.ps1  # Windows PowerShell   ```

| **Response Time** | < 100ms per prediction |

# or: source .venv/bin/activate  # macOS/Linux

---

3. **Run the API locally:**

## 📡 API Endpoints

# 3. Install and run

### 1. GET `/health` - Health Check

pip install -r requirements.txt   ```bash

**Response:**

```jsonpython app.py   # Option A: Using Python directly

{

  "status": "ok",```   python app.py

  "model_loaded": true,

  "uptime_seconds": 156.32

}

```**API will be available at:** `http://localhost:8000`   # Option B: Using uvicorn



**Status Values:**   uvicorn app:app --host 127.0.0.1 --port 8000 --reload

- `"ok"` - Model loaded and ready

- `"degraded"` - App running, model loading on first request### 🔗 Useful Links   ```



---



### 2. POST `/predict` - Get Nutrition Recommendations- **Swagger UI (Interactive Docs):** http://localhost:8000/docs4. **API is now running at:** `http://localhost:8000`



**Request (16 parameters):**- **ReDoc (Alternative Docs):** http://localhost:8000/redoc   - Health check: `http://localhost:8000/health`

```json

{- **Health Check:** http://localhost:8000/health   - Predictions: `http://localhost:8000/predict`

  "Age": 28,

  "Gender": "Female",- **Predictions:** http://localhost:8000/predict (POST)   - Docs: `http://localhost:8000/docs` (auto-generated Swagger UI)

  "Height_cm": 165.0,

  "Weight_kg": 75.0,

  "BMI": 27.5,

  "Exercise_Frequency": 5,---## ✅ Endpoint Testing Results

  "Daily_Steps": 10000,

  "Blood_Pressure_Systolic": 125,

  "Blood_Pressure_Diastolic": 80,

  "Cholesterol_Level": 180,## 🏗️ Architecture"status": "ok",

  "Blood_Sugar_Level": 95,

  "Sleep_Hours": 7.5,"model_loaded": true,

  "Caloric_Intake": 2200,

  "Protein_Intake": 80,```"uptime_seconds": 2.34

  "Carbohydrate_Intake": 250,

  "Fat_Intake": 70┌─────────────────┐}

}

```│   User Request  │



**Response (200 OK):**├─────────────────┤````

```json

{│  FastAPI Router │

  "recommended_calories": 1889,

  "recommended_protein": 84.0,├─────────────────┤**Status:** ✅ PASSED

  "recommended_carbs": 251.9,

  "recommended_fats": 73.9,│ Input Validation│ (Pydantic)**Response Code:** 200 OK

  "bmr": 1480,

  "tdee": 2368,├─────────────────┤

  "health_risk_score": 25,

  "activity_level_score": 6.9│  Load Model*    │ (*lazy load on first request)### Prediction Endpoint Test Results

}

```├─────────────────┤



**Error Codes:**│  Make Prediction│ (scikit-learn)**Request:**

- `422` - Missing/invalid input fields

- `503` - Model download failed├─────────────────┤

- `500` - Model inference error

│ Validate Output │ (Health-safe bounds)```json

---

├─────────────────┤{

### 📝 Request Examples

│  JSON Response  │  "Age": 28,

#### **Using PowerShell:**

```powershell└─────────────────┘  "Gender": "Female",

$payload = @{

  Age = 28```  "Height_cm": 165.0,

  Gender = 'Female'

  Height_cm = 165.0  "Weight_kg": 75.0,

  Weight_kg = 75.0

  BMI = 27.5### Key Components  "BMI": 27.5,

  Exercise_Frequency = 5

  Daily_Steps = 10000  "Exercise_Frequency": 5,

  Blood_Pressure_Systolic = 125

  Blood_Pressure_Diastolic = 80| Component | Details |  "Daily_Steps": 10000,

  Cholesterol_Level = 180

  Blood_Sugar_Level = 95|-----------|---------|  "Blood_Pressure_Systolic": 125,

  Sleep_Hours = 7.5

  Caloric_Intake = 2200| **Framework** | FastAPI 0.104+ with Uvicorn |  "Blood_Pressure_Diastolic": 80,

  Protein_Intake = 80

  Carbohydrate_Intake = 250| **ML Model** | scikit-learn MultiOutputRegressor (Random Forest) |  "Cholesterol_Level": 180,

  Fat_Intake = 70

}| **Model Size** | 125.6 MB (tracked via Git LFS, auto-downloaded) |  "Blood_Sugar_Level": 95,



Invoke-RestMethod -Uri "http://localhost:8000/predict" `| **Python Version** | 3.10+ (tested on 3.11, 3.13) |  "Sleep_Hours": 7.5,

  -Method Post `

  -Body (ConvertTo-Json $payload) `| **Deployment** | Google Cloud Run (2 GB memory, 600s timeout) |  "Caloric_Intake": 2200,

  -ContentType 'application/json'

```| **Response Time** | < 100ms per prediction |  "Protein_Intake": 80,



#### **Using cURL:**  "Carbohydrate_Intake": 250,

```bash

curl -X POST http://localhost:8000/predict \---  "Fat_Intake": 70

  -H "Content-Type: application/json" \

  -d '{}

    "Age": 28,

    "Gender": "Female",## 📡 API Endpoints````

    "Height_cm": 165.0,

    "Weight_kg": 75.0,

    "BMI": 27.5,

    "Exercise_Frequency": 5,### 1. GET `/health` - Health Check**Response:**

    "Daily_Steps": 10000,

    "Blood_Pressure_Systolic": 125,

    "Blood_Pressure_Diastolic": 80,

    "Cholesterol_Level": 180,**Purpose:** Readiness probe and model status check```json

    "Blood_Sugar_Level": 95,

    "Sleep_Hours": 7.5,{

    "Caloric_Intake": 2200,

    "Protein_Intake": 80,**Response:**  "recommended_calories": 1889,

    "Carbohydrate_Intake": 250,

    "Fat_Intake": 70```json  "recommended_protein": 84.0,

  }'

```{  "recommended_carbs": 251.9,



---  "status": "ok",  "recommended_fats": 73.9,



## 🧪 Testing  "model_loaded": true,  "bmr": 1480,



### Run Local Tests  "uptime_seconds": 156.32  "tdee": 2368,



```bash}  "health_risk_score": 25,

# Install test dependencies

pip install -r dev-requirements.txt```  "activity_level_score": 6.9



# Run all tests with verbose output}

pytest test_api.py -v

**Status Values:**```

# Run specific test

pytest test_api.py::test_predict_response_format -v- `"ok"` - Model loaded and ready

`````

- `"degraded"` - App running but model not yet loaded (will load on first /predict)**Status:** ✅ PASSED

### Test Coverage

**Response Code:** 200 OK

| Test | Purpose | Status |

|------|---------|--------|**HTTP Code:** `200 OK`**Processing Time:** < 100ms

| `test_health_endpoint` | Health endpoint returns valid response | ✅ PASSED |

| `test_health_endpoint_fields` | Health response has correct field types | ✅ PASSED |

| `test_predict_endpoint_input_validation` | Predict accepts valid input | ✅ PASSED |

| `test_predict_response_format` | Predict returns all required fields | ✅ PASSED |---## Quick start (developer)

| `test_predict_missing_fields` | Predict validates required fields | ✅ PASSED |

**Test Results:** `5 passed in 3.52s` ✅

### 2. POST `/predict` - Get Nutrition Recommendations1. Create and activate a virtual environment (PowerShell):

### GitHub Actions CI/CD

The project includes pytest workflow that runs on every push:

- Installs dependencies**Purpose:** Get personalized nutrition recommendations based on health metrics```powershell

- Runs all tests with pytest

- Pulls Git LFS filespython -m venv .venv

- Reports results

**Request Body (16 parameters):**.\.venv\Scripts\Activate.ps1

---

`json`

## ☁️ Cloud Deployment

{

### Google Cloud Run

"Age": 28,1. Install dependencies:

**Live URL:** https://gymbite-model-480367101608.europe-west1.run.app

"Gender": "Female",

#### How It Works

"Height_cm": 165.0,```powershell

**Lazy Loading Strategy:**

- App starts in < 1 second (model NOT loaded) "Weight_kg": 75.0,pip install -r requirements.txt

- Model automatically downloads on first `/predict` request from GitHub releases

- Model cached in memory for subsequent requests (< 100ms) "BMI": 27.5,pip install -r dev-requirements.txt # optional: pytest, httpx

#### Model Download Flow "Exercise_Frequency": 5,```

```````"Daily_Steps": 10000,

App Startup

├─ Initialize FastAPI app  "Blood_Pressure_Systolic": 125,1. Run the app locally:

├─ Set up routes

└─ Ready to receive requests  "Blood_Pressure_Diastolic": 80,



First /predict Request  "Cholesterol_Level": 180,```powershell

├─ Check if model exists locally

├─ If missing: Download from GitHub (v1.0 release)  "Blood_Sugar_Level": 95,python -m uvicorn app:app --host 127.0.0.1 --port 8000

├─ Load model into memory

└─ Return prediction  "Sleep_Hours": 7.5,```



Subsequent Requests  "Caloric_Intake": 2200,

└─ Use cached model (< 100ms)

```  "Protein_Intake": 80,## API: POST /predict



#### Configuration  "Carbohydrate_Intake": 250,



- Memory: 2 GB  "Fat_Intake": 70Request: JSON body with the input features. Example shape:

- Timeout: 600 seconds

- Region: europe-west1}

- Platform: Managed

- Ingress: Allow all``````json



#### Deployment Steps{



1. **Create GitHub Release with Model****Successful Response (200 OK):**  "Age": 28,

   - Go to: https://github.com/Nouman13388/gymbite_model/releases

   - Create release with tag: `v1.0````json  "Gender": "Female",

   - Upload: `enhanced_diet_predictor.pkl`

   - Publish{  "Height_cm": 165.0,



2. **Deploy to Cloud Run**  "recommended_calories": 1889,  "Weight_kg": 75.0,

   ```bash

   # Using gcloud CLI  "recommended_protein": 84.0,  "BMI": 27.5,

   gcloud run deploy gymbite-model \

     --source . \  "recommended_carbs": 251.9,  "Exercise_Frequency": 5,

     --platform managed \

     --memory 2Gi \  "recommended_fats": 73.9,  "Daily_Steps": 10000,

     --region europe-west1 \

     --allow-unauthenticated  "bmr": 1480,  "Blood_Pressure_Systolic": 125,

```````

"tdee": 2368, "Blood_Pressure_Diastolic": 80,

3. **Verify Deployment**

   ````bash "health_risk_score": 25,  "Cholesterol_Level": 180,

   # Check health

   curl https://gymbite-model-480367101608.europe-west1.run.app/health  "activity_level_score": 6.9  "Blood_Sugar_Level": 95,



   # Make prediction}  "Sleep_Hours": 7.5,

   curl -X POST https://gymbite-model-480367101608.europe-west1.run.app/predict \

     -H "Content-Type: application/json" \```  "Caloric_Intake": 2200,

     -d '{...}'

   ```  "Protein_Intake": 80,
   ````

#### Troubleshooting**Error Responses:** "Carbohydrate_Intake": 250,

| Issue | Cause | Solution |- `422 Unprocessable Entity` - Missing/invalid input fields "Fat_Intake": 70

|-------|-------|----------|

| Container failed to start | Model not downloading | Check GitHub release exists |- `503 Service Unavailable` - Model download failed}

| Startup timeout | Model loading blocked startup | Lazy loading enabled - works on first request |

| 503 Service Unavailable | Download failed | Verify GitHub release URL accessible |- `500 Internal Server Error` - Model inference error```

| 404 Not Found | Route doesn't exist | Check routes in `app.py` |

---

---Successful response (abridged):

## 💻 Local Development

### Setup

### 📝 Request Examples```json

````bash

# 1. Clone repository{

git clone https://github.com/Nouman13388/gymbite_model.git

cd gymbite_model#### **Using PowerShell:**  "recommended_calories": 1889,



# 2. Create virtual environment```powershell  "recommended_protein": 84.0,

python -m venv .venv

$payload = @{  "recommended_carbs": 251.9,

# Windows PowerShell:

.\.venv\Scripts\Activate.ps1  Age = 28  "recommended_fats": 73.9,



# macOS/Linux:  Gender = 'Female'  "bmr": 1480,

source .venv/bin/activate

  Height_cm = 165.0  "tdee": 2368

# 3. Install dependencies

pip install -r requirements.txt  Weight_kg = 75.0}

pip install -r dev-requirements.txt

  BMI = 27.5```

# 4. Pull model file using Git LFS

git lfs install  Exercise_Frequency = 5

git lfs pull

  Daily_Steps = 10000## Example requests with curl

# 5. Run locally

python app.py  Blood_Pressure_Systolic = 125

````

Blood_Pressure_Diastolic = 80Linux/macOS or Windows with curl installed:

### Project Structure

Cholesterol_Level = 180

````

gymbite_model/  Blood_Sugar_Level = 95```bash

├── app.py                           # FastAPI application

├── enhanced_diet_model.py           # ML predictor class  Sleep_Hours = 7.5curl -X POST http://127.0.0.1:8000/predict \

├── enhanced_diet_predictor.pkl      # Trained model (125.6 MB)

├── requirements.txt                 # Production dependencies  Caloric_Intake = 2200  -H "Content-Type: application/json" \

├── dev-requirements.txt             # Dev dependencies

├── Dockerfile                       # Container spec  Protein_Intake = 80  -d '{

├── cloudbuild.yaml                  # GCP Cloud Build config

├── test_api.py                      # Pytest test cases  Carbohydrate_Intake = 250    "Age": 28,

├── README.md                        # This file

├── Gymbite_API_Collection.postman_collection.json  Fat_Intake = 70    "Gender": "Female",

└── .github/workflows/               # GitHub Actions

    ├── pytest.yml}    "Height_cm": 165.0,

    └── docker-build.yml

```    "Weight_kg": 75.0,



### DependenciesInvoke-RestMethod -Uri "http://localhost:8000/predict" `    "BMI": 27.5,



**Production:**  -Method Post `    "Exercise_Frequency": 5,

- fastapi==0.104.1

- uvicorn[standard]==0.24.0  -Body (ConvertTo-Json $payload) `    "Daily_Steps": 10000,

- pydantic==2.4.2

- scikit-learn==1.3.2  -ContentType 'application/json'    "Blood_Pressure_Systolic": 125,

- pandas==2.0.3

- numpy==1.24.3```    "Blood_Pressure_Diastolic": 80,

- joblib==1.3.2

    "Cholesterol_Level": 180,

**Development:**

- pytest==8.0.2#### **Using cURL:**    "Blood_Sugar_Level": 95,

- httpx==0.25.1

```bash    "Sleep_Hours": 7.5,

### Key Files

curl -X POST http://localhost:8000/predict \    "Caloric_Intake": 2200,

#### `app.py` - FastAPI Application

- **Routes:** `/health` (GET), `/predict` (POST)  -H "Content-Type: application/json" \    "Protein_Intake": 80,

- **Features:** Lazy loading, input validation, error handling

- **Lines:** ~136  -d '{    "Carbohydrate_Intake": 250,



#### `enhanced_diet_model.py` - ML Predictor    "Age": 28,    "Fat_Intake": 70

- **Class:** `EnhancedDietPredictor`

- **Methods:**     "Gender": "Female",  }'

  - `calculate_bmr()` - Basal Metabolic Rate

  - `calculate_tdee()` - Total Daily Energy Expenditure    "Height_cm": 165.0,```

  - `calculate_health_risk_score()` - Health risk assessment

  - `predict()` - Make nutrition predictions    "Weight_kg": 75.0,

- **Lines:** ~160 (production code only)

    "BMI": 27.5,## Example requests with PowerShell

#### `Dockerfile` - Container Spec

- **Base:** python:3.10-slim    "Exercise_Frequency": 5,

- **Port:** 8080 (configurable via PORT env var)

- **Optimized for Cloud Run**    "Daily_Steps": 10000,Windows PowerShell:



---    "Blood_Pressure_Systolic": 125,



## 🔧 Troubleshooting    "Blood_Pressure_Diastolic": 80,```powershell



### Import Error: `enhanced_diet_model not found`    "Cholesterol_Level": 180,$payload = @{

```bash

# Make sure you're in the correct directory    "Blood_Sugar_Level": 95,  Age = 28

ls -la enhanced_diet_model.py

cd /path/to/gymbite_model    "Sleep_Hours": 7.5,  Gender = 'Female'

python app.py

```    "Caloric_Intake": 2200,  Height_cm = 165.0



### Model File Not Found    "Protein_Intake": 80,  Weight_kg = 75.0

```bash

git lfs install    "Carbohydrate_Intake": 250,  BMI = 27.5

git lfs pull

```    "Fat_Intake": 70  Exercise_Frequency = 5



### Port Already in Use  }'  Daily_Steps = 10000

```bash

python -m uvicorn app:app --host 127.0.0.1 --port 9000```  Blood_Pressure_Systolic = 125

````

Blood_Pressure_Diastolic = 80

### Dependencies Missing

```````bash#### **Using Python Requests:**  Cholesterol_Level = 180

pip install -r requirements.txt

``````python  Blood_Sugar_Level = 95



### Cloud Run: Container Failed to Startimport requests  Sleep_Hours = 7.5

- Lazy loading is enabled

- Model loads on first request  Caloric_Intake = 2200

- First `/predict` may take 10-30 seconds (model download)

- Subsequent requests < 100msurl = "http://localhost:8000/predict"  Protein_Intake = 80



### Prediction Returns 503payload = {  Carbohydrate_Intake = 250

```bash

# Verify GitHub release has model file    "Age": 28,  Fat_Intake = 70

curl -I https://github.com/Nouman13388/gymbite_model/releases/download/v1.0/enhanced_diet_predictor.pkl

```    "Gender": "Female",}



### Slow Response on First Request    "Height_cm": 165.0,Invoke-RestMethod -Uri http://127.0.0.1:8000/predict `

**Normal behavior** - First request includes model download (125.6 MB):

- First request: 10-30 seconds (model download)    "Weight_kg": 75.0,  -Method Post `

- Subsequent requests: < 100ms

    # ... (rest of fields)  -Body (ConvertTo-Json $payload) `

---

}  -ContentType 'application/json'

## 📊 Model Performance

```````

### ML Model Details

response = requests.post(url, json=payload)

| Metric | Details |

|--------|---------|print(response.json())## Health / readiness endpoint

| **Type** | Random Forest (n_estimators=100) |

| **Framework** | scikit-learn MultiOutputRegressor |```

| **Target Variables** | 4 (Calories, Protein, Carbs, Fats) |

| **Input Features** | 16 + 5 calculated (21 total) |GET `/health` returns JSON with these fields:

| **Accuracy** | 85%+ (within 10% tolerance) |

| **Output Validation** | Health-safe bounds applied |---

### Calculated Features- `status`: "ok" or "degraded"

- **BMR** - Basal Metabolic Rate (Mifflin-St Jeor equation)## 🧪 Testing- `model_loaded`: boolean

- **TDEE** - Total Daily Energy Expenditure

- **Health Risk Score** - 0-100 risk assessment- `uptime_seconds`: float or null

- **Activity Level Score** - 0-10 activity rating

### Run Local Tests

---

Example healthy response:

## 🚀 Performance

````bash

### Response Times

# Install test dependencies```json

| Scenario | Time |

|----------|------|pip install -r dev-requirements.txt{

| App startup | < 1 second |

| First /predict | 10-30 seconds (model download) |  "status": "ok",

| Subsequent /predict | 50-100ms |

| /health endpoint | < 10ms |# Run all tests with verbose output  "model_loaded": true,



### Scalabilitypytest test_api.py -v  "uptime_seconds": 123.45



- **Cloud Run:** Automatic (0-100+ instances)}

- **Free Tier:** 2 million requests/month

- **Concurrent Requests:** Unlimited on paid tier# Run specific test```



---pytest test_api.py::test_predict_response_format -v



## 🌐 Alternative PlatformsIf the model failed to load at startup, `status` will be `degraded` and `model_loaded` will be `false`. Use this endpoint for readiness probes.



While currently on GCP Cloud Run, can deploy to:# Run with coverage



- **Azure Container Instances**pytest test_api.py --cov=app## 🐳 Docker & Local Deployment

- **AWS Lambda** with API Gateway

- **DigitalOcean App Platform**```

- **Render.com**

- **Railway.app**### Build and Run with Docker

- **Heroku**

### Test Coverage

All require Docker support (provided via `Dockerfile`).

```bash

---

| Test | Purpose | Status |# Build the Docker image

## 📞 Links

|------|---------|--------|docker build -t gymbite_model:local .

- **Repository:** https://github.com/Nouman13388/gymbite_model

- **Live API:** https://gymbite-model-480367101608.europe-west1.run.app| `test_health_endpoint` | Health endpoint returns valid response | ✅ PASSED |

- **Issues:** https://github.com/Nouman13388/gymbite_model/issues

- **Releases:** https://github.com/Nouman13388/gymbite_model/releases| `test_health_endpoint_fields` | Health response has correct field types | ✅ PASSED |# Run the container



---| `test_predict_endpoint_input_validation` | Predict accepts valid input | ✅ PASSED |docker run --rm -p 8000:8000 -v "$PWD:/app" --name gymbite_local gymbite_model:local



**Last Updated:** October 25, 2025  | `test_predict_response_format` | Predict returns all required fields | ✅ PASSED |```

**Status:** ✅ Production Ready

| `test_predict_missing_fields` | Predict validates required fields | ✅ PASSED |

The API will be available at `http://localhost:8000`

**Test Results:** `5 passed in 3.52s` ✅

### Git LFS (Large File Storage)

### GitHub Actions CI/CD

The model file is tracked with Git LFS. To pull it locally:

The project includes pytest workflow that runs on every push to `dev` branch:

- Automatically installs dependencies```bash

- Runs all tests with pytest# Install Git LFS if not already installed

- Pulls Git LFS files for modelgit lfs install

- Reports results to GitHub

# Pull LFS files

---git lfs pull



## ☁️ Cloud Deployment# Verify the model file exists

ls -lh enhanced_diet_predictor.pkl

### Google Cloud Run (Current Deployment)```



**Live URL:** https://gymbite-model-480367101608.europe-west1.run.app## ☁️ Cloud Deployment



#### How It Works### Google Cloud Platform (GCP) - Recommended for Free Tier



1. **Lazy Loading Strategy**Deploy to Google Cloud Run (free tier: 2 million requests/month):

   - App starts in <1 second without loading the 125.6 MB model

   - Model downloads automatically on first `/predict` request from GitHub releases**Current Status:** 🚀 **Live at:** https://gymbite-model-480367101608.europe-west1.run.app

   - Model is cached in memory for all subsequent requests

#### Deployment Notes

2. **Model Download Flow**

   ```The application uses **lazy loading** for the ML model:

   App Startup

   ├─ Initialize FastAPI app- The app starts immediately without loading the model

   ├─ Set up routes- The model loads on the first prediction request

   └─ Ready to receive requests (model NOT loaded)- This avoids startup timeout issues in Cloud Run



   First /predict Request#### Git LFS Model File Handling

   ├─ Check if model file exists locally

   ├─ If missing: Download from GitHub releasesThe model file (`enhanced_diet_predictor.pkl`, 125.6 MB) is tracked with Git LFS. Cloud Build doesn't automatically pull LFS files, so the app has been configured to:

   ├─ Load model into memory

   └─ Return prediction1. Check if the model file exists locally on startup

   2. If missing, download it automatically on the first prediction request

   Subsequent Requests3. Cache it for subsequent requests

   └─ Use cached model (< 100ms)

   ```This ensures the API works seamlessly both locally and in the cloud.



3. **Configuration**### Other Cloud Platforms

   - Memory: 2 GB

   - Timeout: 600 seconds- **Azure Container Instances** - Pay-per-use Docker containers

   - Region: europe-west1- **AWS Lambda** with API Gateway - Serverless option

   - Platform: Managed- **DigitalOcean App Platform** - Simple Docker deployment with free tier

   - Ingress: Allow all- **Render.com** - Free tier available



#### Deployment Steps### Environment Variables (for Cloud Deployment)



1. **Create GitHub Release with Model**Create a `.env.example` file for reference:

````

1.  Go to: https://github.com/Nouman13388/gymbite_model/releases```bash

2.  Click "Create a new release"PORT=8000

3.  Tag: v1.0HOST=0.0.0.0

4.  Upload: enhanced_diet_predictor.pkl (125.6 MB)LOG_LEVEL=info

5.  Publish```

````

## 🔧 Troubleshooting

2. **Deploy to Cloud Run**

```bash- **Model not found:** Run `git lfs pull` to download the model file from Git LFS

# Option A: From GCP Console- **Import errors:** Install dependencies with `pip install -r requirements.txt`

- Go to Cloud Run service- **Port already in use:** Change port with `--port 9000` in uvicorn command

- Click "Edit & deploy new revision"- **Cloud Run startup timeout:** App now uses lazy loading - model loads on first /predict request, not on startup

- Click "Deploy"

## ✅ Testing

# Option B: Using gcloud CLI

gcloud run deploy gymbite-model \Run the test suite locally:

  --source . \

  --platform managed \```bash

  --memory 2Gi \pytest test_api.py -v

  --region europe-west1 \```

  --allow-unauthenticated

```Tests cover:



3. **Verify Deployment**- Health endpoint availability and response format

```bash- Predict endpoint input validation

# Check health- Prediction response format and field types

curl https://gymbite-model-480367101608.europe-west1.run.app/health- Missing field validation

# Make prediction (triggers model download)
curl -X POST https://gymbite-model-480367101608.europe-west1.run.app/predict \
  -H "Content-Type: application/json" \
  -d '{...}'
````

#### Troubleshooting Deployment Issues

| Issue                     | Cause                  | Solution                                               |
| ------------------------- | ---------------------- | ------------------------------------------------------ |
| Container failed to start | Model not downloading  | Check GitHub release exists with model file            |
| Startup timeout           | Model too slow to load | Lazy loading is enabled - model loads on first request |
| 503 Service Unavailable   | Model download failed  | Verify GitHub release URL is accessible                |
| 404 Not Found             | Route doesn't exist    | Check FastAPI routes in `app.py`                       |

---

## 💰 Cost Management

### Automatic Image Cleanup

**Problem:** Each deployment creates a new Docker image in GCP Artifact Registry. Without cleanup, these accumulate and cost ~$0.10/GB/month.

**Solution:** Automated cleanup system that keeps only the 2 most recent images.

#### Option 1: Automated GitHub Actions (Recommended)

**Setup once, runs automatically:**

1. **Create GCP Service Account:**

   ```bash
   # Create service account
   gcloud iam service-accounts create github-actions-cleanup \
     --display-name="GitHub Actions Image Cleanup"

   # Grant permissions
   gcloud projects add-iam-policy-binding gymbite \
     --member="serviceAccount:github-actions-cleanup@gymbite.iam.gserviceaccount.com" \
     --role="roles/artifactregistry.admin"

   # Create key
   gcloud iam service-accounts keys create gcp-key.json \
     --iam-account=github-actions-cleanup@gymbite.iam.gserviceaccount.com
   ```

2. **Add GitHub Secret:**

   - Go to repository Settings → Secrets → Actions
   - Create secret: `GCP_SA_KEY`
   - Paste entire `gcp-key.json` content
   - **Delete local key file:** `rm gcp-key.json`

3. **Push workflow file:**
   ```bash
   git add .github/workflows/cleanup-images.yml
   git commit -m "Add automatic image cleanup"
   git push
   ```

**Runs automatically every Sunday at 2 AM UTC** or manually via GitHub Actions tab.

#### Option 2: Manual Cleanup Script

Run anytime from your local machine:

```powershell
.\cleanup-images.ps1
```

The script will:

- List all current images
- Show how many will be deleted
- Ask for confirmation
- Keep 2 most recent, delete the rest

#### Cost Impact

| Scenario                | Storage | Monthly Cost    |
| ----------------------- | ------- | --------------- |
| No cleanup (40 images)  | ~2 GB   | $0.20           |
| With cleanup (2 images) | ~100 MB | $0.01-0.02      |
| **Savings**             | **95%** | **$0.18/month** |

**Files:**

- `.github/workflows/cleanup-images.yml` - Automated GitHub Actions workflow
- `cleanup-images.ps1` - Manual PowerShell cleanup script
- `CLEANUP_SETUP.md` - Detailed setup instructions

---

## 💻 Local Development

### Setup Development Environment

```bash
# 1. Clone repository
git clone https://github.com/Nouman13388/gymbite_model.git
cd gymbite_model

# 2. Create virtual environment
python -m venv .venv

# Windows PowerShell:
.\.venv\Scripts\Activate.ps1

# macOS/Linux:
source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
pip install -r dev-requirements.txt  # For development and testing

# 4. Pull model file using Git LFS
git lfs install
git lfs pull

# 5. Run locally
python app.py
```

### Directory Structure

```
gymbite_model/
├── app.py                           # Main FastAPI application
├── enhanced_diet_model.py           # ML predictor class (production code only)
├── enhanced_diet_predictor.pkl      # Trained model (125.6 MB)
├── requirements.txt                 # Production dependencies
├── dev-requirements.txt             # Development dependencies
├── Dockerfile                       # Container specification
├── cloudbuild.yaml                  # GCP Cloud Build config
├── test_api.py                      # Pytest test cases
├── README.md                        # This file
├── Gymbite_API_Collection.postman_collection.json  # Postman tests
└── .github/workflows/
    ├── pytest.yml                   # GitHub Actions pytest workflow
    └── docker-build.yml             # Docker build workflow
```

### Dependencies

**Production (`requirements.txt`):**

- fastapi==0.104.1
- uvicorn[standard]==0.24.0
- pydantic==2.4.2
- scikit-learn==1.3.2
- pandas==2.0.3
- numpy==1.24.3
- joblib==1.3.2

**Development (`dev-requirements.txt`):**

- pytest==8.0.2
- httpx==0.25.1

### Code Quality

```bash
# Run tests
pytest test_api.py -v

# Check code style (if flake8 installed)
flake8 app.py enhanced_diet_model.py

# Type checking (if mypy installed)
mypy app.py
```

### Key Files Explained

#### `app.py` - FastAPI Application

- **Purpose:** Main API server
- **Routes:** `/health` (GET), `/predict` (POST)
- **Features:** Lazy loading, input validation, error handling
- **Lines:** ~136

#### `enhanced_diet_model.py` - ML Model Predictor

- **Purpose:** ML inference logic
- **Class:** `EnhancedDietPredictor`
- **Methods:**
  - `calculate_bmr()` - Basal Metabolic Rate
  - `calculate_tdee()` - Total Daily Energy Expenditure
  - `calculate_health_risk_score()` - Health risk assessment
  - `predict()` - Make nutrition predictions
  - `validate_prediction()` - Apply health-safe bounds
- **Lines:** ~160 (production code only)

#### `Dockerfile` - Container Spec

- **Base Image:** python:3.10-slim
- **Exposed Port:** 8080 (configurable via PORT env var)
- **Build:** Multi-stage optimized for Cloud Run
- **Size:** ~500 MB

---

## 🔧 Troubleshooting

### Common Issues and Solutions

#### 1. **Import Error: `enhanced_diet_model not found`**

```
Error: ModuleNotFoundError: No module named 'enhanced_diet_model'
```

**Solution:** Make sure you're in the correct directory and `enhanced_diet_model.py` exists

```bash
ls -la enhanced_diet_model.py
cd /path/to/gymbite_model
python app.py
```

#### 2. **Model File Not Found**

```
Error: FileNotFoundError: enhanced_diet_predictor.pkl not found
```

**Solution:** Pull the model file using Git LFS

```bash
git lfs install
git lfs pull
# Or download manually from GitHub releases
```

#### 3. **Port Already in Use**

```
Error: Address already in use: ('127.0.0.1', 8000)
```

**Solution:** Use a different port

```bash
python -m uvicorn app:app --host 127.0.0.1 --port 9000
```

#### 4. **Dependencies Missing**

```
Error: ModuleNotFoundError: No module named 'fastapi'
```

**Solution:** Install requirements

```bash
pip install -r requirements.txt
```

#### 5. **Cloud Run: Container Failed to Start**

**Solution:** Lazy loading is already implemented. Model loads on first request:

- App starts in <1 second
- First `/predict` request triggers model download
- Subsequent requests use cached model

#### 6. **Prediction Returns 503**

```json
{
  "detail": "Model download failed"
}
```

**Solution:** Verify GitHub release exists with model file

```bash
# Check if release has the model
curl -I https://github.com/Nouman13388/gymbite_model/releases/download/v1.0/enhanced_diet_predictor.pkl
```

#### 7. **Slow Response on First Request**

**Normal behavior:** First request is slow because model is downloading (125.6 MB)

- First request: 10-30 seconds (model download)
- Subsequent requests: < 100ms (cached model)

---

## 📊 Model Performance

### Accuracy Metrics

The model uses scikit-learn Random Forest with MultiOutputRegressor:

| Metric                  | Details                            |
| ----------------------- | ---------------------------------- |
| **Model Type**          | Random Forest (n_estimators=100)   |
| **Target Variables**    | 4 (Calories, Protein, Carbs, Fats) |
| **Input Features**      | 16 + 5 calculated (21 total)       |
| **Prediction Accuracy** | 85%+ (within 10% tolerance)        |
| **Output Validation**   | Health-safe bounds applied         |

### Calculated Features

The model automatically calculates:

- **BMR** - Basal Metabolic Rate (Mifflin-St Jeor equation)
- **TDEE** - Total Daily Energy Expenditure
- **Health Risk Score** - 0-100 risk assessment
- **Activity Level Score** - 0-10 activity rating

---

## 🌐 Alternative Platforms

While currently deployed on GCP Cloud Run, the API can also be deployed on:

- **Azure Container Instances** - Pay-per-use containers
- **AWS Lambda** - Serverless with API Gateway
- **DigitalOcean App Platform** - Simpler alternative
- **Render.com** - Free tier available
- **Railway.app** - Git-based deployment
- **Heroku** - Classic cloud platform

All require Docker support (provided via `Dockerfile`).

---

## 🚀 Performance

### Response Times (Benchmarked)

| Scenario                        | Time          |
| ------------------------------- | ------------- |
| App startup                     | < 1 second    |
| First /predict (model download) | 10-30 seconds |
| Subsequent /predict (cached)    | 50-100ms      |
| /health endpoint                | < 10ms        |

### Scalability

- **Cloud Run scaling:** Automatic (0-100+ instances)
- **Free tier limit:** 2 million requests/month
- **Concurrent requests:** Unlimited on paid tier
- **Model inference:** Single-threaded (per container)

---

## 📝 License

This project is provided as-is for educational and production use.

---

## 👨‍💻 Contributing

To contribute:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🆘 Support

For issues and questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review test files in `test_api.py` for examples
3. Open an issue on GitHub
4. Check FastAPI documentation: https://fastapi.tiangolo.com/

---

## 📞 Contact & Links

- **Repository:** https://github.com/Nouman13388/gymbite_model
- **Live API:** https://gymbite-model-480367101608.europe-west1.run.app
- **Issues:** https://github.com/Nouman13388/gymbite_model/issues
- **Releases:** https://github.com/Nouman13388/gymbite_model/releases

---

**Last Updated:** October 25, 2025  
**Status:** ✅ Production Ready
