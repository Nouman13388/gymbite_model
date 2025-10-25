from typing import Any, Dict, Optional
import time
import logging

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


def create_app() -> FastAPI:
    app = FastAPI(title="Gymbite Nutrition API")

    # instantiate predictor but do not load model yet
    predictor = EnhancedDietPredictor()

    @app.on_event("startup")
    def load_model_on_startup() -> None:
        """Load the trained model once on startup and attach to app.state.

        This marks `app.state.model_loaded` so a /health endpoint can report readiness.
        We avoid raising here so the service can respond to health checks even if the
        model failed to load (the `/predict` endpoint will return 503 in that case).
        """
        app.state.start_time = time.time()
        app.state.model_loaded = False

        try:
            predictor.load_model()  # assumes default path 'enhanced_diet_predictor.pkl'
            app.state.predictor = predictor
            app.state.model_loaded = True
            logger.info("✅ Model loaded successfully on startup")
        except Exception as e:
            # Log but don't crash. The health endpoint will report degraded state.
            logger.error("Failed to load model on startup: %s", e)

    @app.post("/predict")
    async def predict(inp: Input) -> Dict[str, Any]:
        """Accept Input model, run prediction, return JSON result."""
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
