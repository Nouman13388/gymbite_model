# Deployment Plan — FastAPI on Hugging Face Spaces

This document describes the chosen, efficient deployment structure for turning the Gymbite ML project into a production-ready FastAPI service optimized for Hugging Face Spaces.

Summary (chosen architecture)

- Single lightweight `app.py` (single-entry FastAPI application) that imports your existing `EnhancedDietPredictor` class from `enhanced_diet_model.py`.
- Use a lifespan startup event to load the large `.pkl` model once into memory (avoids repeated loads and is fast for request handling).
- Keep the code minimal so it fits Hugging Face Spaces' constraints (single app file + model + supporting modules).

Why this structure?

- Hugging Face Spaces expects a simple entrypoint (single `app.py` for FastAPI). A single-file app is easiest to maintain and deploy there.
- Loading the model on startup (lifespan) is efficient and avoids I/O on every request.
- The app delegates prediction logic to your existing `EnhancedDietPredictor` class — keep model, feature code and business logic in `enhanced_diet_model.py` where it belongs.

Chosen trade-offs

- Single app file for the web layer (keeps repo simple). For larger projects you would split routers, services, and schemas into modules, but for Spaces the single file is most reliable.

---

## File: requirements.txt

Use this final list of dependencies for Hugging Face Spaces (copy into your `requirements.txt`).

```text
numpy
pandas
scikit-learn
joblib
fastapi
uvicorn[standard]
python-multipart
# Optional but recommended for nicer typing on older Python versions
typing-extensions
```

Notes:

- `uvicorn[standard]` installs performant server and recommended extras on Spaces.

- `python-multipart` is optional, but sometimes required by FastAPI for payload handling. It is safe to include.

---

## File: app.py (complete)

Below is the full, copy-pastable `app.py`. It:

- defines the `Input` Pydantic model exactly as shown in your README API contract

- uses a lifespan event to load the model on startup

- exposes POST `/predict` which returns the JSON result of `predictor.predict()`

```python
from typing import Any, Dict
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from enhanced_diet_model import EnhancedDietPredictor


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
        """Load the trained model once on startup and attach to app.state."""
        try:
            predictor.load_model()  # assumes default path 'enhanced_diet_predictor.pkl'
            app.state.predictor = predictor
        except Exception as e:
            # Fail fast — Spaces will show the error in logs
            raise RuntimeError(f"Failed to load model on startup: {e}")

    @app.post("/predict")
    async def predict(inp: Input) -> Dict[str, Any]:
        """Accept Input model, run prediction, return JSON result."""
        pred_service: EnhancedDietPredictor = getattr(app.state, "predictor", None)
        if pred_service is None:
            raise HTTPException(status_code=503, detail="Model not loaded")

        try:
            # predictor.predict expects a dict-like input as in your README
            result = pred_service.predict(inp.dict())
            return result
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
```

Implementation notes

- `EnhancedDietPredictor.load_model()` is called once on startup; it should load `enhanced_diet_predictor.pkl` from the repository root.

- The code attaches the predictor to `app.state.predictor` for thread-safe access inside endpoints.

---

## Local testing

Run the app locally with uvicorn (copy this exact command):

```bash
uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```

Then call the endpoint with curl or a small client. Example `curl` request:

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{"Age":28,"Gender":"Female","Height_cm":165,"Weight_kg":75,"BMI":27.5,"Exercise_Frequency":5,"Daily_Steps":10000,"Blood_Pressure_Systolic":125,"Blood_Pressure_Diastolic":80,"Cholesterol_Level":180,"Blood_Sugar_Level":95,"Sleep_Hours":7.5,"Caloric_Intake":2200,"Protein_Intake":80,"Carbohydrate_Intake":250,"Fat_Intake":70 }'
```

---

## Deployment file list (what to push to Hugging Face Spaces)

Push the following files to the root of your Space repository:

- `app.py` — the FastAPI app (above)
- `enhanced_diet_model.py` — your model wrapper and feature engineering code
- `enhanced_diet_predictor.pkl` — the trained model binary (if it's large, consider using Git LFS or host externally and download in startup)
- `requirements.txt` — the dependency list (see above)
- `README.md` — optional, user-facing docs (keeps project clear)
- `.gitignore` — optional, to prevent committing new large binaries

Optional but recommended

- `start.sh` — a small runner script for custom startup (not required on Spaces)

- `utils/` — optional helper modules

---

## Final notes and troubleshooting

- If the `.pkl` model is >100MB, Hugging Face Git-backed Spaces will reject the push. Use Git LFS or host the model externally and modify `load_model()` to download it at startup.

- On Spaces, the default command used to run a FastAPI app is `uvicorn app:app --host 0.0.0.0 --port $PORT` — Spaces sets `$PORT` automatically.

- If the model takes long to load, consider printing progress messages in `load_model()` so logs show activity.

If you want, I can also:

- Add a small `start_model_download()` helper to `app.py` that downloads the `.pkl` from a public URL at startup (useful if you host the model on S3 or a release asset).

- Create a minimal `Dockerfile` for local containerized testing.
