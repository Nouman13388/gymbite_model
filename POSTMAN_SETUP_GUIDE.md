# Gymbite API - Postman Collection Setup Guide

## 📋 Overview

This guide helps developers import and use the Gymbite Nutrition API collection in Postman for testing, development, and integration.

## 🚀 Quick Start - Import Collection

### Option 1: Import from File (Recommended)

1. **Open Postman** on your machine
2. **Click "Import"** button (top-left corner)
3. **Select "Upload Files"** tab
4. **Choose** `Gymbite_API_Collection.postman_collection.json`
5. **Click "Import"**
6. ✅ Collection will appear in your workspace!

### Option 2: Import from Link

1. **Click "Import"** in Postman
2. **Paste this URL:**
   ```
   [Your GitHub raw file URL - if hosted on GitHub]
   ```
3. **Click "Import"**

### Option 3: Manual Setup

1. Create a new collection named "Gymbite Nutrition API"
2. Create folders:
   - Health & Status
   - Nutrition Predictions
3. Add requests following the API documentation below

## 🔧 Configuration

### ⚠️ IMPORTANT - Endpoint Configuration

**The collection is pre-configured for LOCAL DEVELOPMENT** on `http://localhost:8000`.

#### Getting Started - LOCAL TESTING (Recommended for Development)

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Nouman13388/gymbite_model.git
   cd gymbite_model
   ```

2. **Pull the model file from Git LFS:**

   ```bash
   git lfs install
   git lfs pull
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Start the API locally:**

   ```bash
   # Option A: Using Python directly
   python app.py

   # Option B: Using uvicorn
   uvicorn app:app --host 127.0.0.1 --port 8000 --reload
   ```

5. **API is now running at:** `http://localhost:8000`

   - Health check: `http://localhost:8000/health`
   - Predictions: `http://localhost:8000/predict`
   - Documentation: `http://localhost:8000/docs`

6. **Use Postman Collection:** With the default `base_url = http://localhost:8000`, all requests will work immediately!

#### For CLOUD DEPLOYMENT (GCP, AWS, Azure)

If you deploy to a cloud platform:

1. **Get your deployed API URL** from your cloud provider
2. **Select Collection** → "Gymbite Nutrition API"
3. **Go to "Variables"** tab
4. **Update `base_url`** to your deployed endpoint:

   ```text
   https://your-cloud-endpoint.com
   ```

5. **Example for GCP Cloud Run:**

   ```text
   https://gymbite-model-xxxxx-us-central1.a.run.app
   ```

   https://your-api-endpoint.com

   ```

   ```

**Important Notes:**

- ❌ **HF Spaces Direct Access:** The app is deployed on HF Spaces but endpoints are not publicly exposed
- ✅ **Local Testing:** Run locally for full API access via Postman
- ✅ **Cloud Options:** Deploy to HF Inference Endpoints, AWS, Azure, or other platforms for external API access

### Environment Setup (Optional)

Create environments if you need to switch between URLs frequently:

1. **Click "Environments"** (left sidebar)
2. **Create Environment** → Name: "Gymbite - Production"
3. **Add Variables:**

   ```
   base_url: https://huggingface.co/spaces/Nouman1338/gymbite-model
   ```

4. **Create another environment** → Name: "Gymbite - Local Dev" (if needed)
5. **Add Variables:**

   ```
   base_url: http://localhost:8000
   ```

## 📚 API Endpoints

### 1. Health Check - GET /health

**Endpoint:** `{{base_url}}/health`

**Full URL (Production):** `https://huggingface.co/spaces/Nouman1338/gymbite-model/health`

**Purpose:** Verify API is running and model is loaded

**Method:** GET

**Response (200 OK):**

```json
{
  "status": "ok",
  "model_loaded": true,
  "uptime_seconds": 16.8
}
```

**Use Cases:**

- Health monitoring
- CI/CD pipeline verification
- Load balancer health checks

---

### 2. Get Nutrition Recommendation - POST /predict

**Endpoint:** `{{base_url}}/predict`

**Full URL (Production):** `https://huggingface.co/spaces/Nouman1338/gymbite-model/predict`

**Purpose:** Get personalized nutrition recommendations based on user health data

**Method:** POST

**Headers:**

```
Content-Type: application/json
Accept: application/json
```

**Request Body (16 Parameters):**

| Parameter                | Type    | Description                     | Example  |
| ------------------------ | ------- | ------------------------------- | -------- |
| Age                      | integer | User age in years               | 28       |
| Gender                   | string  | "Male", "Female", or "Other"    | "Female" |
| Height_cm                | float   | Height in centimeters           | 165.0    |
| Weight_kg                | float   | Weight in kilograms             | 75.0     |
| BMI                      | float   | Body Mass Index                 | 27.5     |
| Exercise_Frequency       | integer | Days per week of exercise (0-7) | 5        |
| Daily_Steps              | integer | Average daily steps             | 10000    |
| Blood_Pressure_Systolic  | integer | Systolic pressure (mmHg)        | 125      |
| Blood_Pressure_Diastolic | integer | Diastolic pressure (mmHg)       | 80       |
| Cholesterol_Level        | integer | Total cholesterol (mg/dL)       | 180      |
| Blood_Sugar_Level        | integer | Fasting blood sugar (mg/dL)     | 95       |
| Sleep_Hours              | float   | Average sleep per night         | 7.5      |
| Caloric_Intake           | integer | Daily caloric intake            | 2200     |
| Protein_Intake           | integer | Daily protein (grams)           | 80       |
| Carbohydrate_Intake      | integer | Daily carbs (grams)             | 250      |
| Fat_Intake               | integer | Daily fat (grams)               | 70       |

**Example Request:**

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

**Response (200 OK):**

| Field                | Type    | Description                    |
| -------------------- | ------- | ------------------------------ |
| recommended_calories | float   | Daily calorie target           |
| recommended_protein  | float   | Daily protein target (grams)   |
| recommended_carbs    | float   | Daily carbs target (grams)     |
| recommended_fats     | float   | Daily fat target (grams)       |
| bmr                  | integer | Basal Metabolic Rate           |
| tdee                 | integer | Total Daily Energy Expenditure |
| health_risk_score    | integer | Health risk score (0-100)      |
| activity_level_score | float   | Activity level score           |

**Example Response:**

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

---

## 📝 Sample Requests

The collection includes 3 pre-configured sample requests:

1. **Get Nutrition Recommendation** (Default example - moderate activity)
2. **Sample Request - Active Male** (High activity, good health)
3. **Sample Request - Sedentary Female** (Low activity, elevated risks)

Use these to quickly test the API with realistic data!

---

## 🧪 Testing Tips

### 1. Test Health Endpoint First

Always verify the API is up before testing predictions:

- Send GET /health request
- Confirm `model_loaded: true`

### 2. Use Environment Variables

Replace hardcoded URLs with `{{base_url}}` for easy switching between environments

### 3. Save Responses

Postman automatically saves responses - useful for comparing different user profiles

### 4. Create Request Collections by Use Case

Organize requests by feature:

- Nutrition prediction requests
- Health monitoring requests
- Integration test requests

### 5. Use Scripts for Automation

Add pre-request script to validate data:

```javascript
// Validate Age is reasonable
const age = pm.request.body.raw.Age;
if (age < 1 || age > 150) {
  throw new Error("Invalid age");
}
```

Add test script to validate responses:

```javascript
pm.test("Response has all required fields", function () {
  const response = pm.response.json();
  pm.expect(response).to.have.property("recommended_calories");
  pm.expect(response).to.have.property("bmr");
  pm.expect(response).to.have.property("health_risk_score");
});
```

---

## 🔐 Authentication (If Added in Future)

When authentication is implemented:

1. **Go to Collection Settings**
2. **Authorization** tab
3. **Type:** Bearer Token / API Key
4. **Token:** `{{auth_token}}`

Add to environment variables:

```
auth_token: your-token-here
```

---

## 🚀 Deployment Endpoints

### Local Development

```
http://localhost:8000
```

### Hugging Face Spaces (Production)

```
https://huggingface.co/spaces/Nouman1338/gymbite-model
```

**Note:** Update base_url variable when switching environments!

---

## 📊 API Specifications

- **API Type:** REST (JSON)
- **Framework:** FastAPI
- **Response Format:** JSON
- **Content-Type:** application/json
- **Request Timeout:** 30 seconds (recommended)

---

## 🐛 Troubleshooting

| Issue              | Solution                                                                      |
| ------------------ | ----------------------------------------------------------------------------- |
| 404 Not Found      | Check base_url variable is correct; ensure trailing slash is NOT included     |
| 500 Internal Error | Verify all 16 required fields in request                                      |
| Model not loaded   | Restart API server; check model file exists                                   |
| Slow responses     | Check server resources; model loads on first request                          |
| Connection refused | Ensure API server is running                                                  |
| HF Spaces 404      | Use full URL: `https://huggingface.co/spaces/Nouman1338/gymbite-model/health` |
| HF Spaces timeout  | HF Spaces can be slow; increase timeout in Postman settings                   |

### HF Spaces Specific Tips

If you're testing against Hugging Face Spaces and getting 404 errors:

1. **Verify the URL format:**

   - ❌ Wrong: `https://huggingface.co/spaces/Nouman1338/gymbite-model/` (trailing slash)
   - ✅ Correct: `https://huggingface.co/spaces/Nouman1338/gymbite-model`

2. **Test health endpoint first:**

   - Go to: `https://huggingface.co/spaces/Nouman1338/gymbite-model/health`
   - Should return: `{"status": "ok", "model_loaded": true}`

3. **Increase timeout for HF Spaces:**

   - Go to Postman Settings → General → Request Timeout (ms)
   - Set to at least 60000 (60 seconds)

4. **If Space is sleeping:**
   - Visit the Space URL directly to wake it up
   - Then retry your requests

---

## 📞 Support Resources

- **GitHub Repository:** https://github.com/Nouman13388/gymbite_model
- **Live Demo:** https://huggingface.co/spaces/Nouman1338/gymbite-model
- **Issues:** Open issue on GitHub repository

---

## 👥 Team Sharing

### Share Collection with Team

1. **Right-click Collection** → "Share"
2. **Copy Share Link**
3. **Send to team members**
4. They can import via link!

### Alternative: Upload to GitHub

1. Commit `Gymbite_API_Collection.postman_collection.json` to repository
2. Team members clone and import locally
3. Ensures everyone has latest version

---

## 📈 Integration Examples

### cURL

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"Age": 28, "Gender": "Female", "Height_cm": 165.0, ...}'
```

### Python (requests)

```python
import requests

data = {
    "Age": 28,
    "Gender": "Female",
    "Height_cm": 165.0,
    # ... other fields
}

response = requests.post("http://localhost:8000/predict", json=data)
print(response.json())
```

### JavaScript (fetch)

```javascript
fetch("http://localhost:8000/predict", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    Age: 28,
    Gender: "Female",
    Height_cm: 165.0,
    // ... other fields
  }),
})
  .then((r) => r.json())
  .then((data) => console.log(data));
```

---

## ✅ Version

- **Collection Version:** 1.0.0
- **API Version:** 1.0.0
- **Last Updated:** October 25, 2025

---

**Happy Testing! 🎉**
