#!/usr/bin/env python3
"""
Test Gymbite API endpoints
Tests both health and prediction endpoints with model pre-loaded
"""

import sys
import os
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from enhanced_diet_model import EnhancedDietPredictor
from fastapi.testclient import TestClient

def test_endpoints():
    """Test endpoints with model loaded"""
    
    print("=" * 80)
    print("🧪 GYMBITE API ENDPOINT TESTING")
    print("=" * 80)
    print()
    
    # Create app
    app = create_app()
    
    # Pre-load model
    print("Loading ML model...")
    predictor = EnhancedDietPredictor()
    try:
        predictor.load_model('enhanced_diet_predictor.pkl')
        app.state.predictor = predictor
        app.state.model_loaded = True
        print("✅ Model loaded successfully\n")
    except Exception as e:
        print(f"❌ Failed to load model: {e}\n")
        return 1
    
    client = TestClient(app)
    
    # Test 1: Health endpoint
    print("1️⃣  TESTING HEALTH ENDPOINT")
    print("-" * 80)
    print("GET /health")
    print()
    
    try:
        response = client.get("/health")
        
        if response.status_code == 200:
            print(f"✅ SUCCESS (Status: {response.status_code})")
            print()
            print("Response:")
            print(json.dumps(response.json(), indent=2))
            health_passed = True
        else:
            print(f"❌ FAILED (Status: {response.status_code})")
            health_passed = False
    except Exception as e:
        print(f"❌ FAILED: {e}")
        health_passed = False
    
    print()
    print()
    
    # Test 2: Prediction endpoint
    print("2️⃣  TESTING PREDICTION ENDPOINT")
    print("-" * 80)
    print("POST /predict")
    print()
    
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
    
    print("Request Payload:")
    print(json.dumps(payload, indent=2))
    print()
    
    try:
        response = client.post("/predict", json=payload)
        
        if response.status_code == 200:
            print(f"✅ SUCCESS (Status: {response.status_code})")
            print()
            print("Response:")
            prediction = response.json()
            print(json.dumps(prediction, indent=2))
            predict_passed = True
        else:
            print(f"❌ FAILED (Status: {response.status_code})")
            print(f"Response: {response.text}")
            predict_passed = False
    except Exception as e:
        print(f"❌ FAILED: {e}")
        predict_passed = False
    
    print()
    print()
    print("=" * 80)
    print("📊 TEST SUMMARY")
    print("=" * 80)
    print(f"Health Endpoint:     {'✅ PASSED' if health_passed else '❌ FAILED'}")
    print(f"Prediction Endpoint: {'✅ PASSED' if predict_passed else '❌ FAILED'}")
    print()
    
    if health_passed and predict_passed:
        print("🎉 ALL TESTS PASSED!")
        print()
        return 0
    else:
        print("⚠️  SOME TESTS FAILED")
        print()
        return 1

if __name__ == "__main__":
    exit_code = test_endpoints()
    sys.exit(exit_code)
