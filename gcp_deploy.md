# Google Cloud Run Deployment Guide for Gymbite

Complete step-by-step instructions to deploy Gymbite Nutrition API to Google Cloud Run.

## 📋 Prerequisites

Before starting, ensure you have:

1. **Google Cloud Account:** [Create one here](https://cloud.google.com/)
2. **Google Cloud SDK installed:** [Installation guide](https://cloud.google.com/sdk/docs/install)
3. **Project created on GCP:** [Create a new project](https://console.cloud.google.com/projectcreate)
4. **GitHub repository set up** with the Gymbite code

---

## 🚀 Step-by-Step Deployment

### Step 1: Install Google Cloud SDK

If not already installed, download and install from: `https://cloud.google.com/sdk/docs/install`

Verify installation:

```bash
gcloud --version
```

### Step 2: Initialize and Authenticate

Set up your Google Cloud environment:

```bash
# Initialize gcloud
gcloud init

# This will open a browser window to authenticate
# Follow the prompts to sign in with your Google account
```

Verify you're authenticated:

```bash
gcloud auth list
```

### Step 3: Set Your GCP Project

Replace `YOUR-PROJECT-ID` with your actual GCP project ID:

```bash
# Set the default project
gcloud config set project YOUR-PROJECT-ID

# Verify the project is set
gcloud config get-value project
```

### Step 4: Enable Required Google Cloud Services

These services are required for the deployment:

```bash
# Enable Cloud Run
gcloud services enable run.googleapis.com

# Enable Cloud Build (to build Docker images in the cloud)
gcloud services enable cloudbuild.googleapis.com

# Enable Artifact Registry (to store Docker images)
gcloud services enable artifactregistry.googleapis.com

# Enable Container Registry (alternative to Artifact Registry)
gcloud services enable containerregistry.googleapis.com
```

Verify services are enabled:

```bash
gcloud services list --enabled | grep -E "run|cloudbuild|artifact|container"
```

### Step 5: Build Docker Image Using Cloud Build

Cloud Build compiles your Docker image in the cloud (no need to build locally).

```bash
# Build the image and store it in Artifact Registry
# Replace REGION with your preferred region (e.g., us-central1, europe-west1)
gcloud builds submit \
  --region=REGION \
  --tag REGION-docker.pkg.dev/YOUR-PROJECT-ID/gymbite/gymbite-model:latest

# Alternative: Use Container Registry (simpler)
gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/gymbite-model:latest
```

**Example with us-central1 and Container Registry:**

```bash
gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/gymbite-model:latest
```

Monitor the build progress in the Cloud Console:

- Open: `https://console.cloud.google.com/cloud-build/builds`

### Step 6: Deploy to Cloud Run

Deploy your built image as a Cloud Run service:

```bash
gcloud run deploy gymbite-model \
  --image gcr.io/YOUR-PROJECT-ID/gymbite-model:latest \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --timeout 3600 \
  --set-env-vars LOG_LEVEL=info
```

**Parameters explanation:**

| Parameter | Value | Purpose |
|-----------|-------|---------|
| `deploy` | `gymbite-model` | Service name |
| `--image` | `gcr.io/...` | Docker image location |
| `--platform` | `managed` | Managed Cloud Run (recommended) |
| `--region` | `us-central1` | GCP region (adjust as needed) |
| `--allow-unauthenticated` | | Make API public (no authentication) |
| `--memory` | `512Mi` | Memory allocation (512 MB sufficient) |
| `--timeout` | `3600` | Request timeout in seconds (1 hour) |
| `--set-env-vars` | `LOG_LEVEL=info` | Environment variables |

**Common Regions:**

```bash
us-central1       # Iowa
us-east1          # South Carolina
europe-west1      # Belgium
asia-east1        # Taiwan
```

### Step 7: Get Your Service URL

Once deployment completes, retrieve your service URL:

```bash
gcloud run services describe gymbite-model --region us-central1

# Extract just the URL
gcloud run services describe gymbite-model \
  --region us-central1 \
  --format 'value(status.url)'
```

**Output will look like:**

```text
https://gymbite-model-xxxxxxxxxxxxx-uc.a.run.app
```

### Step 8: Test Your Deployment

Test your API endpoints:

```bash
# Test the health endpoint
curl https://your-service-url/health

# Test the prediction endpoint
curl -X POST https://your-service-url/predict \
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

---

## 🔄 Updating Your Postman Collection

After deployment, update your Postman collection with the production URL:

1. Open **Gymbite_API_Collection.postman_collection.json** in Postman
2. Go to **Variables** tab
3. Update `base_url`:

   ```text
   https://gymbite-model-xxxxxxxxxxxxx-uc.a.run.app
   ```

4. Save and test all endpoints

---

## 📊 Monitoring and Logs

### View Deployment Logs

```bash
# View recent logs
gcloud run services describe gymbite-model --region us-central1

# Stream live logs
gcloud logging read "resource.type=cloud_run_revision AND resource.labels.service_name=gymbite-model" \
  --region us-central1 \
  --limit 50 \
  --format json

# Or use the Cloud Console
# https://console.cloud.google.com/run
```

### View Service Details

```bash
gcloud run services describe gymbite-model --region us-central1
```

### Check Memory and CPU Usage

```bash
# Get more detailed metrics (requires Cloud Monitoring)
gcloud monitoring timeseries list \
  --filter 'resource.type="cloud_run_revision" AND resource.labels.service_name="gymbite-model"'
```

---

## 🔒 Advanced Configuration

### Set Custom Domain

```bash
gcloud run domain-mappings create \
  --service=gymbite-model \
  --domain=api.yourdomain.com \
  --region=us-central1
```

### Configure Autoscaling

```bash
# Scale up to 100 instances maximum
gcloud run services update gymbite-model \
  --max-instances=100 \
  --region us-central1

# Set minimum instances (always running)
gcloud run services update gymbite-model \
  --min-instances=1 \
  --region us-central1
```

### Set Concurrency

```bash
# Allow 80 concurrent requests per instance
gcloud run services update gymbite-model \
  --concurrency=80 \
  --region us-central1
```

### Add Environment Variables

```bash
gcloud run services update gymbite-model \
  --update-env-vars \
  LOG_LEVEL=debug,DEBUG_MODE=true \
  --region us-central1
```

---

## 💰 Cost Estimation

**Free Tier (Per Month):**

- 2,000,000 requests
- 180,000 GB-seconds (compute time)
- Sufficient for testing and light production use

**Example Costs:**

| Scenario | Estimated Cost |
|----------|---|
| 1M requests/month, 50GB-seconds | $0 (within free tier) |
| 5M requests/month, 200GB-seconds | ~$0.50-1.00 |
| 100M requests/month (production) | ~$10-30 |

Check GCP pricing: `https://cloud.google.com/run/pricing`

---

## 🔧 Troubleshooting

### Issue: "Image pull failed"

**Solution:** Ensure the image exists in Cloud Registry:

```bash
# List all images in gcr.io
gcloud container images list

# Check specific image
gcloud container images list-tags gcr.io/YOUR-PROJECT-ID/gymbite-model
```

### Issue: "Model not found" error

**Solution:** Ensure Git LFS files are included:

```bash
# In your local repository
git lfs pull

# Before pushing/building
git lfs ls-files
```

### Issue: "Permission denied" or authentication errors

**Solution:** Re-authenticate:

```bash
gcloud auth login
gcloud auth application-default login
```

### Issue: Service timeout (504 errors)

**Solution:** Increase timeout and memory:

```bash
gcloud run services update gymbite-model \
  --timeout=3600 \
  --memory=1Gi \
  --region us-central1
```

### Issue: High latency on first request (cold start)

**Solution:** Set minimum instances to keep one instance warm:

```bash
gcloud run services update gymbite-model \
  --min-instances=1 \
  --region us-central1
```

---

## 📚 Complete Deployment Script

Save this as `deploy.sh` for quick future deployments:

```bash
#!/bin/bash

# Configuration
PROJECT_ID="YOUR-PROJECT-ID"
SERVICE_NAME="gymbite-model"
REGION="us-central1"
IMAGE_NAME="gymbite-model"

# Set project
gcloud config set project $PROJECT_ID

# Enable services
echo "Enabling Google Cloud services..."
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Build image
echo "Building Docker image with Cloud Build..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/$IMAGE_NAME:latest

# Deploy to Cloud Run
echo "Deploying to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --image gcr.io/$PROJECT_ID/$IMAGE_NAME:latest \
  --platform managed \
  --region $REGION \
  --allow-unauthenticated \
  --memory 512Mi \
  --timeout 3600

# Get service URL
echo ""
echo "Deployment complete!"
gcloud run services describe $SERVICE_NAME --region $REGION --format 'value(status.url)'
```

**Usage:**

```bash
# Make it executable
chmod +x deploy.sh

# Run it
./deploy.sh
```

---

## ✅ Deployment Checklist

- [ ] Google Cloud Account created
- [ ] gcloud SDK installed and authenticated
- [ ] GCP Project created
- [ ] All required services enabled
- [ ] Docker image built with Cloud Build
- [ ] Service deployed to Cloud Run
- [ ] Service URL obtained and tested
- [ ] Postman collection updated with production URL
- [ ] Health endpoint returning 200 OK
- [ ] Prediction endpoint tested successfully
- [ ] Monitoring and alerts configured (optional)
- [ ] Custom domain configured (optional)

---

## 📖 Additional Resources

- **Cloud Run Documentation:** `https://cloud.google.com/run/docs`
- **Cloud Build Documentation:** `https://cloud.google.com/build/docs`
- **Artifact Registry:** `https://cloud.google.com/artifact-registry/docs`
- **gcloud CLI Reference:** `https://cloud.google.com/sdk/gcloud/reference`
- **Pricing Calculator:** `https://cloud.google.com/products/calculator`

---

## 🎯 Next Steps

1. **Deploy using the steps above**
2. **Share the service URL with your team**
3. **Update Postman collection with production URL**
4. **Monitor logs and performance**
5. **Configure custom domain (optional)**
6. **Set up alerts and monitoring (optional)**

Happy deploying! 🚀
