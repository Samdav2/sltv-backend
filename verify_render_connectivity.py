import requests
import json

RENDER_BASE_URL = "https://sltv-backend-1.onrender.com/api/v1/services/tv"

def test_connectivity():
    print(f"Testing connectivity to {RENDER_BASE_URL}...")
    try:
        # We expect 405 Method Not Allowed for GET on POST endpoints, or 422 Validation Error if we POST empty data
        # This confirms the server is up and the path exists.

        # Test Details Endpoint
        print("Checking /details...")
        response = requests.post(f"{RENDER_BASE_URL}/details", json={}, timeout=10)
        print(f"Response Code: {response.status_code}")
        print(f"Response: {response.text[:200]}")

        # Test Refresh Endpoint
        print("\nChecking /refresh...")
        response = requests.post(f"{RENDER_BASE_URL}/refresh", json={}, timeout=10)
        print(f"Response Code: {response.status_code}")
        print(f"Response: {response.text[:200]}")

        # Test Purchase Endpoint
        print("\nChecking / (Purchase)...")
        response = requests.post(f"{RENDER_BASE_URL}", json={}, timeout=10)
        print(f"Response Code: {response.status_code}")
        print(f"Response: {response.text[:200]}")

    except Exception as e:
        print(f"Connection failed: {e}")

if __name__ == "__main__":
    test_connectivity()
