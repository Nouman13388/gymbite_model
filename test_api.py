"""Simple smoke tests for Gymbite API endpoints."""
import pytest
from fastapi.testclient import TestClient
from app import app


client = TestClient(app)


def test_health_endpoint():
    """Test that /health endpoint returns a response"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data
    assert "model_loaded" in data
    assert "uptime_seconds" in data


def test_health_endpoint_fields():
    """Test that /health returns correct field types"""
    response = client.get("/health")
    data = response.json()
    assert isinstance(data["status"], str)
    assert data["status"] in ["ok", "degraded"]
    assert isinstance(data["model_loaded"], bool)


def test_predict_endpoint_input_validation():
    """Test that /predict accepts valid input"""
    payload = {
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
    response = client.post("/predict", json=payload)
    # Should return 200 or 503 (model not loaded, will download)
    assert response.status_code in [200, 503]


def test_predict_response_format():
    """Test that /predict returns expected fields when model is loaded"""
    payload = {
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
    response = client.post("/predict", json=payload)
    
    if response.status_code == 200:
        data = response.json()
        # Check that all expected fields are present
        expected_fields = [
            'recommended_calories',
            'recommended_protein',
            'recommended_carbs',
            'recommended_fats',
            'bmr',
            'tdee',
            'health_risk_score',
            'activity_level_score'
        ]
        for field in expected_fields:
            assert field in data, f"Missing field: {field}"
        
        # Check that values are numeric
        assert isinstance(data['recommended_calories'], (int, float))
        assert isinstance(data['recommended_protein'], (int, float))
        assert isinstance(data['bmr'], (int, float))


def test_predict_missing_fields():
    """Test that /predict validates required fields"""
    payload = {
        "Age": 28,
        "Gender": "Female",
        # Missing all other required fields
    }
    response = client.post("/predict", json=payload)
    # Should return 422 (validation error)
    assert response.status_code == 422
