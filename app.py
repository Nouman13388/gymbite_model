from typing import Any, Dict, Optional
import time
import logging
import os
import urllib.request
import json
from pathlib import Path

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv

from enhanced_diet_model import EnhancedDietPredictor

# Load environment variables from .env file
load_dotenv()

# Load configuration
def load_config():
    config_path = Path(__file__).parent / "config.json"
    with open(config_path, 'r') as f:
        return json.load(f)

CONFIG = load_config()

# Logger setup
logger = logging.getLogger("gymbite")


class Input(BaseModel):
    # Health & Biometric Data
    Age: int
    Gender: str
    Height_cm: float
    Weight_kg: float
    BMI: float
    Exercise_Frequency: int
    Daily_Steps: int
    Blood_Pressure_Systolic: int
    Blood_Pressure_Diastolic: int
    Cholesterol_Level: int
    Blood_Sugar_Level: int
    Sleep_Hours: float
    Caloric_Intake: float
    Protein_Intake: float
    Carbohydrate_Intake: float
    Fat_Intake: float
    
    # User Preference Fields (with defaults)
    Region: Optional[str] = "Global"
    City: Optional[str] = None
    Dietary_Preference: Optional[str] = "omnivore"  # omnivore, vegetarian, vegan, halal, kosher, pescatarian
    Fitness_Goal: Optional[str] = "maintenance"  # weight_loss, muscle_gain, maintenance, cutting, bulking, athletic
    Goal_Timeline: Optional[str] = "moderate"  # aggressive, moderate, conservative
    Meal_Frequency: Optional[int] = 3  # 2-6 meals per day
    Excluded_Ingredients: Optional[list[str]] = []
    Allergens: Optional[list[str]] = []
    Budget_Level: Optional[str] = "medium"  # low, medium, high
    Cooking_Time: Optional[str] = "moderate"  # quick, moderate, elaborate
    Cuisine_Preference: Optional[str] = "local"  # local, international, fusion
    Meal_Timing_Preference: Optional[str] = "balanced"  # balanced, front_loaded, back_loaded


class MealPlanRequest(BaseModel):
    """Request schema for meal plan generation with user preferences"""
    # Nutritional targets (from /predict endpoint)
    total_calories: int
    total_protein: float
    total_carbs: float
    total_fats: float
    
    # Meal distribution
    meals: list[Dict[str, Any]]  # From meal_distribution in /predict response
    
    # User preferences (from dietary_constraints)
    region: str = "Global"
    city: Optional[str] = None
    dietary_preference: str = "omnivore"
    excluded_ingredients: list[str] = []
    allergens: list[str] = []
    budget_level: str = "medium"
    cooking_time: str = "moderate"
    cuisine_preference: str = "local"
    meal_timing_preference: str = "balanced"


def download_model_from_github() -> None:
    """Download the model file from GitHub releases if not present locally."""
    # Get values from environment or config
    owner = os.getenv('MODEL_OWNER', CONFIG['model']['default_owner'])
    repo = os.getenv('MODEL_REPO', CONFIG['model']['default_repo'])
    version = os.getenv('MODEL_VERSION', CONFIG['model']['default_version'])
    filename = os.getenv('MODEL_FILENAME', CONFIG['model']['default_filename'])
    
    # Use custom URL if provided, otherwise build from template
    model_url = os.getenv('MODEL_DOWNLOAD_URL')
    if not model_url:
        url_template = CONFIG['model']['download_url_template']
        model_url = url_template.format(owner=owner, repo=repo, version=version, filename=filename)
    
    model_file = filename
    
    logger.info(f"Downloading model from {model_url}...")
    try:
        urllib.request.urlretrieve(model_url, model_file)
        logger.info(f"✅ Model downloaded successfully to {model_file}")
    except Exception as e:
        logger.error(f"Failed to download model: {e}")
        raise


def create_app() -> FastAPI:
    app = FastAPI(title="Gymbite Nutrition API")

    # instantiate predictor but do not load model yet
    predictor = EnhancedDietPredictor()
    
    # Configure Gemini API
    gemini_api_key = os.getenv('GEMINI_API_KEY')
    if gemini_api_key:
        os.environ['GOOGLE_API_KEY'] = gemini_api_key
        app.state.gemini_client = genai.Client()
        # Store model name from env or config
        app.state.gemini_model = os.getenv('GEMINI_MODEL', CONFIG['gemini']['default_model'])
        logger.info(f"✅ Gemini API configured successfully with model: {app.state.gemini_model}")
    else:
        app.state.gemini_client = None
        app.state.gemini_model = None
        logger.warning("⚠️ GEMINI_API_KEY not found - meal generation will be unavailable")

    @app.on_event("startup")
    def startup() -> None:
        """Minimal startup - don't load model, just initialize state."""
        app.state.start_time = time.time()
        app.state.model_loaded = False
        app.state.predictor = None
        logger.info("✅ FastAPI app started successfully - model will load on first /predict request")

    def load_model_lazy() -> None:
        """Load model on first request if not already loaded."""
        if getattr(app.state, "model_loaded", False):
            return  # Already loaded

        # Download model if missing
        model_filename = os.getenv('MODEL_FILENAME', CONFIG['model']['default_filename'])
        if not os.path.exists(model_filename):
            logger.info("Downloading model from GitHub...")
            try:
                download_model_from_github()
            except Exception as e:
                logger.error(f"Failed to download model: {e}")
                raise HTTPException(status_code=503, detail="Model download failed")

        try:
            predictor.load_model(model_filename, CONFIG)
            app.state.predictor = predictor
            app.state.model_loaded = True
            logger.info(f"✅ Model loaded successfully from {model_filename}")
        except Exception as e:
            logger.error("Failed to load model: %s", e)
            raise

    @app.post("/predict")
    async def predict(inp: Input) -> Dict[str, Any]:
        """Accept Input model, run prediction, return JSON result."""
        # Load model on first request if not loaded
        load_model_lazy()

        pred_service: EnhancedDietPredictor = getattr(app.state, "predictor", None)
        if pred_service is None:
            raise HTTPException(status_code=503, detail="Model not loaded")

        try:
            # predictor.predict expects a dict-like input as in your README
            # Use Pydantic v2's `model_dump()` to avoid v1 `dict()` deprecation
            result = pred_service.predict(inp.model_dump())
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/generate-meal-plan")
    async def generate_meal_plan(request: MealPlanRequest) -> Dict[str, Any]:
        """
        Generate personalized meal plan using Gemini API.
        Requires GEMINI_API_KEY environment variable.
        """
        gemini_client = getattr(app.state, "gemini_client", None)
        if gemini_client is None:
            raise HTTPException(
                status_code=503, 
                detail="Meal generation unavailable - GEMINI_API_KEY not configured"
            )

        # Build excluded items list
        excluded_items = request.excluded_ingredients + request.allergens
        excluded_str = ', '.join(excluded_items) if excluded_items else 'None'

        # Create Gemini prompt
        prompt = f"""You are a professional nutritionist and chef specializing in {request.region} cuisine.

**CLIENT PROFILE (MUST RESPECT ALL REQUIREMENTS):**
- Location: {request.region}{f", {request.city}" if request.city else ""}
- Dietary Preference: {request.dietary_preference} (STRICT - NO EXCEPTIONS)
- Cuisine Style: {request.cuisine_preference}
- Budget Level: {request.budget_level}
- Cooking Time Available: {request.cooking_time}
- EXCLUDED Ingredients: {excluded_str}
- ALLERGENS to AVOID: {', '.join(request.allergens) if request.allergens else 'None'}
- Meal Timing Preference: {request.meal_timing_preference}

**NUTRITIONAL REQUIREMENTS:**
- Total Daily Calories: {request.total_calories} kcal
- Total Protein: {request.total_protein}g
- Total Carbs: {request.total_carbs}g
- Total Fats: {request.total_fats}g

**MEAL BREAKDOWN:**
{chr(10).join([f"- {m['meal']}: {m['calories']} kcal ({m['protein']}g protein, {m['carbs']}g carbs, {m['fats']}g fats)" for m in request.meals])}

**STRICT REQUIREMENTS:**
1. Use ONLY ingredients commonly available in {request.region}
2. Respect {request.dietary_preference} dietary rules with ZERO violations
3. NEVER include: {excluded_str}
4. Match {request.cuisine_preference} cooking style from {request.region}
5. Budget-appropriate for {request.budget_level} income level in {request.region}
6. Cooking time must match {request.cooking_time} preference
7. Provide realistic portion sizes in local measurements (grams, cups, pieces)

**OUTPUT FORMAT (JSON ONLY, NO MARKDOWN):**
{{
  "meal_plan": {{
    "breakfast": {{
      "name": "Dish name",
      "ingredients": ["ingredient 1 (amount)", "ingredient 2 (amount)"],
      "calories": 500,
      "protein": 25,
      "carbs": 60,
      "fats": 15,
      "prep_time_minutes": 15,
      "cooking_instructions": "Step-by-step instructions"
    }},
    "lunch": {{ ... }},
    "dinner": {{ ... }}
  }},
  "nutritional_summary": {{
    "total_calories": {request.total_calories},
    "total_protein": {request.total_protein},
    "total_carbs": {request.total_carbs},
    "total_fats": {request.total_fats}
  }},
  "compliance_verification": {{
    "dietary_preference_met": true,
    "allergens_avoided": true,
    "excluded_ingredients_avoided": true,
    "region_appropriate": true
  }}
}}

Generate the meal plan now. Return ONLY valid JSON, no markdown formatting."""

        try:
            # Call Gemini API with configured model
            gemini_model = getattr(app.state, "gemini_model", CONFIG['gemini']['default_model'])
            response = gemini_client.models.generate_content(
                model=gemini_model,
                contents=prompt
            )
            response_text = response.text.strip()
            
            # Remove markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()
            
            # Parse JSON response
            meal_plan_data = json.loads(response_text)
            
            return {
                "success": True,
                "meal_plan": meal_plan_data.get("meal_plan", {}),
                "nutritional_summary": meal_plan_data.get("nutritional_summary", {}),
                "compliance_verification": meal_plan_data.get("compliance_verification", {}),
                "user_preferences": {
                    "region": request.region,
                    "dietary_preference": request.dietary_preference,
                    "budget_level": request.budget_level
                }
            }
            
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse Gemini response: {e}")
            logger.error(f"Response text: {response_text[:500]}")
            raise HTTPException(
                status_code=500,
                detail="Failed to parse meal plan response. Please try again."
            )
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Meal generation failed: {str(e)}"
            )

    @app.get("/health")
    async def health() -> Dict[str, Optional[Any]]:
        """Health and readiness endpoint.

        Returns JSON with overall status, whether the model is loaded, and uptime (seconds).
        - status: "ok" when model loaded, "degraded" otherwise
        - model_loaded: boolean
        - uptime_seconds: float or null if not available
        """
        model_loaded = getattr(app.state, "model_loaded", False)
        start: Optional[float] = getattr(app.state, "start_time", None)
        uptime = (time.time() - start) if start is not None else None
        status = "ok" if model_loaded else "degraded"
        return {"status": status, "model_loaded": model_loaded, "uptime_seconds": uptime}

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    host = os.getenv('HOST', CONFIG['server']['default_host'])
    port = int(os.getenv('PORT', CONFIG['server']['default_port']))
    uvicorn.run(app, host=host, port=port)

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
