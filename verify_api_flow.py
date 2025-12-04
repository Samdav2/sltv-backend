import sys
import os
from fastapi.testclient import TestClient
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set mock credentials if missing to pass Settings validation
if not os.getenv("MAIL_JET_API"):
    os.environ["MAIL_JET_API"] = "mock_api_key"
if not os.getenv("MAIL_JET_SECRET"):
    os.environ["MAIL_JET_SECRET"] = "mock_secret_key"
if not os.getenv("MAIL_FROM"):
    os.environ["MAIL_FROM"] = "test@example.com"

# Mock other required settings
if not os.getenv("MOBILENIG_PUBLIC_KEY"):
    os.environ["MOBILENIG_PUBLIC_KEY"] = "mock_mobile_public"
if not os.getenv("MOBILENIG_SECRET_KEY"):
    os.environ["MOBILENIG_SECRET_KEY"] = "mock_mobile_secret"
if not os.getenv("PAYSTACK_PUBLIC_KEY"):
    os.environ["PAYSTACK_PUBLIC_KEY"] = "mock_paystack_public"
if not os.getenv("PAYSTACK_SECRET_KEY"):
    os.environ["PAYSTACK_SECRET_KEY"] = "mock_paystack_secret"

# Add project root to path
sys.path.append(os.getcwd())

from app.main import app

client = TestClient(app)

def verify_api_flow():
    print("Verifying API Flow...")

    email = "adoxop_test_integrated_2@gmail.com"
    password = "SecurePassword123!"
    full_name = "Test User Integrated 2"

    # 1. Register
    print("\n1. Testing Registration...")
    register_data = {
        "email": email,
        "password": password,
        "full_name": full_name,
        "phone_number": "08012345678"
    }

    # Registration endpoint is /api/v1/users/
    response = client.post("/api/v1/users/", json=register_data)
    if response.status_code == 200 or response.status_code == 201:
        print("  [OK] Registration successful.")
    elif response.status_code == 400 and "already exists" in response.text:
        print("  [INFO] User already registered. Proceeding to login.")
    else:
        print(f"  [FAIL] Registration failed: {response.status_code} - {response.text}")
        # Proceed to login anyway in case it failed because of something else but user exists

    # 2. Login
    print("\n2. Testing Login...")
    login_data = {
        "username": email, # OAuth2PasswordRequestForm uses 'username' for email
        "password": password
    }

    # Login endpoint is /api/v1/auth/login/access-token
    response = client.post("/api/v1/auth/login/access-token", data=login_data)
    if response.status_code == 200:
        print("  [OK] Login successful.")
        token_data = response.json()
        access_token = token_data.get("access_token")
        token_type = token_data.get("token_type")
        headers = {"Authorization": f"{token_type} {access_token}"}
        print(f"  [INFO] Access Token retrieved.")
    else:
        print(f"  [FAIL] Login failed: {response.status_code} - {response.text}")
        return # Cannot proceed without token

    # 3. Get Profile
    print("\n3. Testing Get Profile...")
    # Profile endpoint is /api/v1/profile/me
    response = client.get("/api/v1/profile/me", headers=headers)
    if response.status_code == 200:
        profile = response.json()
        print(f"  [OK] Profile retrieved: {profile}")
        # Note: UserProfileRead does not return email, so we can't verify it here.
        # But successful retrieval means token is valid and linked to a user.
    elif response.status_code == 404:
        print("  [INFO] Profile not found (expected if not created yet). Creating profile...")
        # Create profile
        profile_data = {
            "phone_number": "08012345678",
            "address": "123 Test St",
            "state": "Lagos",
            "lga": "Ikeja"
        }
        response = client.post("/api/v1/profile/me", headers=headers, json=profile_data)
        if response.status_code == 200:
             print("  [OK] Profile created successfully.")
             print(f"  [INFO] Profile Data: {response.json()}")
        else:
             print(f"  [FAIL] Profile creation failed: {response.status_code} - {response.text}")
    else:
        print(f"  [FAIL] Get Profile failed: {response.status_code} - {response.text}")

    # 4. Check Wallet (if possible)
    # Since we don't have a direct wallet endpoint in the list (api.py showed wallet.router but we didn't check endpoints),
    # we'll skip for now or try /api/v1/wallet/balance if we want to guess.
    # Let's check api.py again... it has wallet.router at /wallet.
    # Let's try GET /api/v1/wallet/balance or /api/v1/wallet/
    print("\n4. Checking Wallet...")
    response = client.get("/api/v1/wallet/balance", headers=headers) # Guessing endpoint
    if response.status_code == 200:
        print(f"  [OK] Wallet Balance: {response.json()}")
    elif response.status_code == 404:
         # Try root
         response = client.get("/api/v1/wallet/", headers=headers)
         if response.status_code == 200:
             print(f"  [OK] Wallet Info: {response.json()}")
         else:
             print(f"  [INFO] Could not guess wallet endpoint. Status: {response.status_code}")
    else:
        print(f"  [INFO] Wallet check failed: {response.status_code}")

if __name__ == "__main__":
    verify_api_flow()
