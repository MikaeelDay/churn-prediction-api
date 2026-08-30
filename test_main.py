from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message" : "Hello World"
    }

def test_secure_data_without_key():
    response = client.get("/secure-data")
    assert response.status_code == 422

def test_secure_data_with_wrong_key():
    response = client.get("/secure-data", headers={"X-API-KEY": "wrong_key"})
    assert response.status_code == 401


def test_secure_data_with_correct_key():
    response = client.get("/secure-data", headers={"X-API-KEY":"my-secret-key-123"})
    assert response.status_code == 200
    assert response.json() == {"data":"this information is secure"}
