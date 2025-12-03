import pytest
from fastapi.testclient import TestClient

@pytest.mark.anyio
async def test_create_user(client: TestClient):
    response = client.post(
        "/api/v1/users/",
        json={"email": "test@example.com", "password": "password", "full_name": "Test User"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

@pytest.mark.anyio
async def test_login(client: TestClient):
    # Create user first
    client.post(
        "/api/v1/users/",
        json={"email": "test@example.com", "password": "password"},
    )

    response = client.post(
        "/api/v1/auth/login/access-token",
        data={"username": "test@example.com", "password": "password"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    return data["access_token"]

@pytest.mark.anyio
async def test_wallet_funding(client: TestClient):
    token = await test_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/api/v1/wallet/fund?amount=500",
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["amount"] == 500.0
    assert data["type"] == "credit"

@pytest.mark.anyio
async def test_airtime_purchase(client: TestClient):
    token = await test_login(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Fund wallet first
    client.post("/api/v1/wallet/fund?amount=500", headers=headers)

    response = client.post(
        "/api/v1/services/airtime",
        headers=headers,
        json={"phone_number": "08012345678", "amount": 100, "network": "MTN"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["message"] == "Airtime purchase processing"
