from typing import Any, Dict, Optional
import time
import logging
import os
import urllib.request

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from enhanced_diet_model import EnhancedDietPredictor

# Logger setup
logger = logging.getLogger("gymbite")


class Input(BaseModel):
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


def download_model_from_github() -> None:
    """Download the model file from GitHub releases if not present locally."""
    model_url = "https://github.com/Nouman13388/gymbite_model/releases/download/v1.0/enhanced_diet_predictor.pkl"
    model_file = "enhanced_diet_predictor.pkl"
    
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
        if not os.path.exists("enhanced_diet_predictor.pkl"):
            logger.info("Downloading model from GitHub...")
            try:
                download_model_from_github()
            except Exception as e:
                logger.error(f"Failed to download model: {e}")
                raise HTTPException(status_code=503, detail="Model download failed")

        try:
            predictor.load_model()  # assumes default path 'enhanced_diet_predictor.pkl'
            app.state.predictor = predictor
            app.state.model_loaded = True
            logger.info("✅ Model loaded successfully on first request")
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

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
