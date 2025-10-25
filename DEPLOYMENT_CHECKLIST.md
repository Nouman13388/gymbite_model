# Deployment Checklist

Use this checklist to prepare your Gymbite deployment.

## Pre-Deployment

- [x] App imports without errors
- [x] `/health` endpoint implemented and returns correct JSON
- [x] `/predict` endpoint implemented and tested
- [x] README.md updated with API documentation
- [x] Example curl and PowerShell requests provided
- [x] Docker image builds successfully
- [x] All changes committed to GitHub
- [ ] Choose deployment platform (see QUICK START below)

## Local Testing (Before Any Deployment)

```powershell
# 1. Test app locally
python -m uvicorn app:app --host 127.0.0.1 --port 8000

# 2. In another terminal, test health endpoint
curl http://127.0.0.1:8000/health

# 3. Test prediction endpoint
$payload = @{
  Age = 28; Gender = 'Female'; Height_cm = 165.0; Weight_kg = 75.0; BMI = 27.5;
  Exercise_Frequency = 5; Daily_Steps = 10000; Blood_Pressure_Systolic = 125;
  Blood_Pressure_Diastolic = 80; Cholesterol_Level = 180; Blood_Sugar_Level = 95;
  Sleep_Hours = 7.5; Caloric_Intake = 2200; Protein_Intake = 80;
  Carbohydrate_Intake = 250; Fat_Intake = 70
}
Invoke-RestMethod -Uri http://127.0.0.1:8000/predict -Method Post -Body (ConvertTo-Json $payload) -ContentType 'application/json'
```

- [ ] `/health` returns `status: ok` and `model_loaded: true`
- [ ] `/predict` returns valid nutrition recommendations
- [ ] No errors in console

## Docker Local Test

```powershell
docker build -t gymbite_model:test .
docker run --rm -p 7860:7860 -v "${PWD}:/app" --name gymbite_test gymbite_model:test
```

- [ ] Docker image builds without errors
- [ ] Container starts successfully
- [ ] `/health` returns `status: ok`
- [ ] Model loads (check logs for "model loaded" message)

## Choose Your Deployment Platform

### Option 1: Hugging Face Spaces (Recommended)
Free, easy, perfect for ML projects

1. [ ] Create account at https://huggingface.co
2. [ ] Create new Space with Docker SDK
3. [ ] Get your Space URL
4. [ ] Run: `git remote add hf https://huggingface.co/spaces/YOUR_USERNAME/gymbite-model`
5. [ ] Run: `git push hf dev:main`
6. [ ] Wait 2-5 minutes for build to complete
7. [ ] [ ] Test health endpoint on deployed URL
8. [ ] [ ] Test prediction endpoint on deployed URL
9. [ ] [ ] Save Space URL

### Option 2: Docker Hub
Share your Docker image publicly

1. [ ] Create account at https://hub.docker.com
2. [ ] Create repository named `gymbite-model`
3. [ ] Run: `docker login`
4. [ ] Run: `docker build -t YOUR_USERNAME/gymbite-model:latest .`
5. [ ] Run: `docker push YOUR_USERNAME/gymbite-model:latest`
6. [ ] [ ] Verify image on Docker Hub
7. [ ] [ ] Image is public and pullable

### Option 3: Render.com
Auto-deploys from GitHub, free tier available

1. [ ] Create account at https://render.com
2. [ ] Go to Dashboard → New Web Service
3. [ ] Connect your GitHub repository
4. [ ] Set name: `gymbite-model`
5. [ ] Set environment: Docker
6. [ ] Click "Create Web Service"
7. [ ] [ ] Wait for build to complete
8. [ ] [ ] Get Render-provided URL
9. [ ] [ ] Test health endpoint

### Option 4: Railway.app
Simple deployment, auto-deploys on push

1. [ ] Create account at https://railway.app
2. [ ] Create new project
3. [ ] Connect GitHub repository
4. [ ] Railway auto-detects Dockerfile
5. [ ] Set environment variable: `PORT=7860`
6. [ ] [ ] Wait for deploy to complete
7. [ ] [ ] Get Railway URL
8. [ ] [ ] Test health endpoint

### Option 5: Local Docker (for testing/staging)

1. [ ] Run: `docker build -t gymbite_model:local .`
2. [ ] Run: `docker run -p 7860:7860 -v "${PWD}:/app" gymbite_model:local`
3. [ ] [ ] Access at `http://localhost:7860`
4. [ ] [ ] Test `/health` endpoint

## Post-Deployment Testing

### Test Health Endpoint

```bash
curl https://your-deployed-url/health
```

Expected response:
```json
{
  "status": "ok",
  "model_loaded": true,
  "uptime_seconds": 123.45
}
```

- [ ] Response status code is 200
- [ ] `status` is "ok"
- [ ] `model_loaded` is `true`
- [ ] `uptime_seconds` is a number

### Test Prediction Endpoint

```powershell
$payload = @{
  Age = 28; Gender = 'Female'; Height_cm = 165.0; Weight_kg = 75.0; BMI = 27.5;
  Exercise_Frequency = 5; Daily_Steps = 10000; Blood_Pressure_Systolic = 125;
  Blood_Pressure_Diastolic = 80; Cholesterol_Level = 180; Blood_Sugar_Level = 95;
  Sleep_Hours = 7.5; Caloric_Intake = 2200; Protein_Intake = 80;
  Carbohydrate_Intake = 250; Fat_Intake = 70
}
Invoke-RestMethod -Uri https://your-deployed-url/predict -Method Post -Body (ConvertTo-Json $payload) -ContentType 'application/json'
```

- [ ] Response status code is 200
- [ ] Response includes `recommended_calories`
- [ ] Response includes `recommended_protein`
- [ ] Response includes `recommended_carbs`
- [ ] Response includes `recommended_fats`
- [ ] Response includes `bmr` and `tdee`

## Production Setup

- [ ] Enable HTTPS/SSL (most platforms do this automatically)
- [ ] Set up monitoring/alerting
- [ ] Configure logging
- [ ] Set up automatic backups if needed
- [ ] Document API for users
- [ ] Share deployment URL with stakeholders
- [ ] Set up rate limiting if needed
- [ ] Configure CORS if consumed from web frontend
- [ ] Add authentication/API keys if needed

## Documentation

- [ ] README.md has quick start guide
- [ ] API endpoints documented
- [ ] Example requests provided
- [ ] Health endpoint documented
- [ ] Troubleshooting section included

## Maintenance

- [ ] Set up log monitoring
- [ ] Set up uptime monitoring
- [ ] Plan for model updates
- [ ] Plan for dependency updates
- [ ] Document rollback procedure
- [ ] Set up automated backups

## Done!

Congratulations! Your Gymbite ML model is now deployed and ready to serve nutrition recommendations.

### Useful Commands

```powershell
# View deployment logs
docker logs gymbite_local

# Scale horizontally (on Kubernetes)
kubectl scale deployment gymbite --replicas 3

# Monitor health
while($true) { curl https://your-url/health; Start-Sleep 60 }

# Load test (requires Apache Bench or similar)
# ab -n 100 -c 10 https://your-url/health
```

### Support & Troubleshooting

- Model not loading? Check Git LFS: `git lfs pull`
- Unpickle warnings? Ensure `scikit-learn==1.7.0` in requirements.txt
- Port already in use? Change port in docker run or environment variable
- Need to rollback? `git revert HEAD && git push`

---

**🚀 Happy deploying!**
