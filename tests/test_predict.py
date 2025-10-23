from fastapi.testclient import TestClient
from app import app


sample = {
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
    "Fat_Intake": 70,
}


def test_predict_endpoint():
    """Integration-style unit test: start app, POST sample payload, assert 200 and expected keys."""
    with TestClient(app) as client:
        resp = client.post("/predict", json=sample)

    assert resp.status_code == 200, f"Unexpected status: {resp.status_code} - {resp.text}"
    data = resp.json()

    # Basic shape assertions
    for key in ("recommended_calories", "recommended_protein", "recommended_carbs", "recommended_fats"):
        assert key in data, f"Missing key in response: {key}"

    # numeric checks
    assert isinstance(data.get("recommended_calories"), (int, float))
    assert isinstance(data.get("recommended_protein"), (int, float))
from fastapi.testclient import TestClient
from app import app

sample = {
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


def run_test():
    # Use context manager so startup/shutdown events are executed
    with TestClient(app) as client:
        resp = client.post("/predict", json=sample)
    print("status_code:", resp.status_code)
    try:
        print("json:", resp.json())
    except Exception as e:
        print("response text:", resp.text)


if __name__ == '__main__':
    run_test()
