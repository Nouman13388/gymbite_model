# Quick Deployment Guide

## 🚀 Deploy to Render (5 Minutes)

### Step 1: Get Gemini API Key

1. Visit: https://aistudio.google.com/apikey
2. Click "Create API Key"
3. Copy the key (starts with `AIza...`)

### Step 2: Update Render Environment

1. Go to: https://dashboard.render.com
2. Select your service: `gymbite-model`
3. Go to "Environment" tab
4. Click "Add Environment Variable"
5. Add:
   - **Key:** `GEMINI_API_KEY`
   - **Value:** Paste your API key
6. Click "Save Changes"

### Step 3: Deploy

Render will automatically redeploy when you:

- Push to GitHub (if auto-deploy enabled), OR
- Click "Manual Deploy" → "Deploy latest commit"

Wait 3-5 minutes for deployment to complete.

### Step 4: Test

```bash
# Test 1: Health check
GET https://gymbite-model.onrender.com/health

# Test 2: Enhanced prediction
POST https://gymbite-model.onrender.com/predict
# Use Postman: "Sample Request - Active Male"

# Test 3: Meal generation
POST https://gymbite-model.onrender.com/generate-meal-plan
# Use Postman: "Generate Meal Plan - Pakistani Halal"
```

---

## 📋 Pre-Deployment Checklist

- [ ] Gemini API key obtained from Google AI Studio
- [ ] Environment variable added to Render
- [ ] Latest code pushed to GitHub (if using auto-deploy)
- [ ] Postman collection imported and base_url set

---

## 🧪 Testing Order

1. **Health Check** → Verify service is running
2. **Predict (old format)** → Test backward compatibility
3. **Predict (new format)** → Test enhanced features
4. **Generate Meal Plan** → Test Gemini integration

---

## ⚡ Common Issues

### "GEMINI_API_KEY not configured"

- **Cause:** Environment variable not set
- **Fix:** Add to Render Environment tab

### "Model not loaded" on first request

- **Cause:** Cold start (model downloading)
- **Fix:** Wait 30-60 seconds, retry

### "Failed to parse meal plan response"

- **Cause:** Gemini returned markdown instead of JSON
- **Fix:** Code handles this automatically, check logs

### 503 Service Unavailable

- **Cause:** Render service sleeping (15min inactivity)
- **Fix:** Wait for wake-up, or set up UptimeRobot

---

## 📊 Expected Response Times

| Endpoint            | Cold Start | Warm    |
| ------------------- | ---------- | ------- |
| /health             | < 5s       | < 100ms |
| /predict            | 30-60s     | < 500ms |
| /generate-meal-plan | 35-65s     | 5-10s   |

---

## 🎯 Demo Script (For Evaluation)

### Show 1: Enhanced Personalization

```
1. Open Postman
2. Send "Sample Request - Active Male"
3. Highlight new fields: Region, Dietary_Preference, Fitness_Goal
4. Show response: meal_distribution, dietary_constraints
5. Explain: "28 inputs vs competitors' 5"
```

### Show 2: Regional Meal Generation

```
1. Send "Generate Meal Plan - Pakistani Halal"
2. Point out response: "Aloo Paratha", "Chicken Karahi"
3. Show compliance_verification: all true
4. Explain: "Culturally authentic, not generic Western food"
```

### Show 3: Dietary Compliance

```
1. Send "Generate Meal Plan - Vegan Weight Loss"
2. Show excluded_ingredients: ["soy"]
3. Verify response has no soy-based dishes
4. Explain: "AI respects all dietary restrictions"
```

### Show 4: Fitness Goal Optimization

```
1. Compare two requests:
   - Same user, Fitness_Goal: "weight_loss"
   - Same user, Fitness_Goal: "muscle_gain"
2. Show calorie difference (-500 vs +400)
3. Show macro split changes
4. Explain: "18 goal combinations vs competitors' 1-2"
```

---

## 💰 Cost Breakdown (Show to Evaluators)

| Service                | Monthly Usage | Cost      |
| ---------------------- | ------------- | --------- |
| Render (512MB)         | 750 hrs       | $0.00     |
| Gemini API             | ~500 calls    | $0.00     |
| GitHub (model storage) | 125MB         | $0.00     |
| **Total**              |               | **$0.00** |

**Competitors:** $5-10/month for hosting alone

---

## 🔮 Future Enhancements (If Asked)

### Week 3 (Optional):

- Response caching (7-day TTL) → 60% fewer Gemini calls
- Rate limiting (10 req/min) → Prevent abuse
- UptimeRobot monitoring → Prevent cold starts

### Week 4+ (Stretch):

- Local recipe database (30+ recipes)
- User feedback collection
- Multi-language support (Urdu, Hindi, Arabic)
- Mobile app integration (React Native)

---

## 📞 Quick Links

- **Production API:** https://gymbite-model.onrender.com
- **Gemini API Dashboard:** https://aistudio.google.com/apikey
- **Render Dashboard:** https://dashboard.render.com
- **GitHub Repo:** https://github.com/Nouman13388/gymbite_model
- **Postman Collection:** Import from `Gymbite_API_Collection.postman_collection.json`

---

## ✅ Deployment Verification

After deployment, verify:

- [ ] GET /health returns `{"status": "ok", "model_loaded": true}`
- [ ] POST /predict works with old format (backward compatible)
- [ ] POST /predict returns new fields (meal_distribution, dietary_constraints)
- [ ] POST /generate-meal-plan returns culturally appropriate meals
- [ ] Response times < 10s for meal generation (warm)

---

**Status:** Implementation Complete ✅  
**Next Step:** Deploy to Render and test endpoints  
**Time Required:** 5 minutes setup + 3 minutes deployment
