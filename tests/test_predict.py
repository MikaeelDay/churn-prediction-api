from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

VALID_PAYLOAD = {
    "gender": "Female",
    "SeniorCitizen": 0,
    "Partner": "Yes",
    "Dependents": "No",
    "tenure": 12,
    "PhoneService": "Yes",
    "MultipleLines": "No",
    "InternetService": "Fiber optic",
    "OnlineSecurity": "No",
    "OnlineBackup": "Yes",
    "DeviceProtection": "No",
    "TechSupport": "No",
    "StreamingTV": "Yes",
    "StreamingMovies": "No",
    "Contract": "Month-to-month",
    "PaperlessBilling": "Yes",
    "PaymentMethod": "Electronic check",
    "MonthlyCharges": 70.35,
    "TotalCharges": 845.5,
}

HEADERS = {"X-API-Key": "my-secret-key-123"}


def test_predict_success():
    response = client.post("/predict", json=VALID_PAYLOAD, headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["churn_prediction"] in ["Yes", "No"]
    assert 0 <= data["churn_probability"] <= 1


def test_predict_without_api_key():
    response = client.post("/predict", json=VALID_PAYLOAD)
    assert response.status_code == 422  # چون هدر اجباریه و نیومده


def test_predict_with_wrong_api_key():
    response = client.post("/predict", json=VALID_PAYLOAD, headers={"X-API-Key": "wrong"})
    assert response.status_code == 401


def test_predict_with_invalid_input():
    bad_payload = VALID_PAYLOAD.copy()
    bad_payload["InternetService"] = "Satellite"  # مقداری که توی Literal تعریف نکردیم
    response = client.post("/predict", json=bad_payload, headers=HEADERS)
    assert response.status_code == 422