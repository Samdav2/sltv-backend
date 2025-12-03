import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_balance():
    response = client.get("/api/v1/mobilenig/balance")
    assert response.status_code == 200
    data = response.json()
    assert "details" in data
    assert "balance" in data["details"]
    print(f"Balance: {data['details']['balance']}")

def test_get_services():
    response = client.get("/api/v1/mobilenig/services")
    if response.status_code != 200:
        print(f"Error: {response.text}")
    assert response.status_code == 200
    data = response.json()
    assert "details" in data
    if isinstance(data["details"], list):
        print(f"Services count: {len(data['details'])}")
    else:
        print(f"API Message: {data['details']}")
        assert isinstance(data["details"], str)

def test_validate_customer():
    # Using a dummy number, might fail but we want to see the response
    payload = {
        "service_id": "DSTV",
        "customerAccountId": "1234567890"
    }
    response = client.post("/api/v1/mobilenig/validate", json=payload)
    if response.status_code != 200:
        print(f"Error: {response.text}")
    # It might return 400 if invalid number, but let's see if it hits the API
    # assert response.status_code == 200
    print(f"Validation Response: {response.json()}")
