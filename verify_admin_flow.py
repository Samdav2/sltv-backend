import sys
import os
from fastapi.testclient import TestClient
from dotenv import load_dotenv
from sqlmodel import Session, select, create_engine

# Load environment variables
load_dotenv()

# Set mock credentials if missing
if not os.getenv("MAIL_JET_API"):
    os.environ["MAIL_JET_API"] = "mock_api_key"
if not os.getenv("MAIL_JET_SECRET"):
    os.environ["MAIL_JET_SECRET"] = "mock_secret_key"
if not os.getenv("MAIL_FROM"):
    os.environ["MAIL_FROM"] = "test@example.com"
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
from app.core.config import settings
from app.models.user import User

client = TestClient(app)

def make_user_superuser(email: str):
    """Helper to make a user a superuser directly in DB"""
    engine = create_engine(settings.DATABASE_URL)
    with Session(engine) as session:
        statement = select(User).where(User.email == email)
        user = session.exec(statement).first()
        if user:
            user.is_superuser = True
            session.add(user)
            session.commit()
            session.refresh(user)
            print(f"  [INFO] User {email} promoted to SUPERUSER.")
        else:
            print(f"  [FAIL] User {email} not found for promotion.")

def verify_admin_flow():
    print("Verifying Admin Flow...")

    admin_email = "admin_test@example.com"
    admin_password = "AdminPassword123!"

    # 1. Register Admin User (initially normal)
    print("\n1. Registering Admin User...")
    register_data = {
        "email": admin_email,
        "password": admin_password,
        "full_name": "Admin User",
        "phone_number": "08099999999"
    }
    response = client.post("/api/v1/users/", json=register_data)
    if response.status_code in [200, 201]:
        print("  [OK] Admin user registered.")
    elif response.status_code == 400 and "already exists" in response.text:
        print("  [INFO] Admin user already exists.")
    else:
        print(f"  [FAIL] Registration failed: {response.status_code}")
        return

    # 2. Promote to Superuser (Direct DB manipulation)
    make_user_superuser(admin_email)

    # 3. Login as Admin
    print("\n2. Logging in as Admin...")
    login_data = {
        "username": admin_email,
        "password": admin_password
    }
    response = client.post("/api/v1/auth/login/access-token", data=login_data)
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data.get("access_token")
        headers = {"Authorization": f"Bearer {access_token}"}
        print("  [OK] Admin logged in.")
    else:
        print(f"  [FAIL] Admin login failed: {response.status_code}")
        return

    # 4. Test User Management Endpoints
    print("\n3. Testing Admin User Management...")

    # List Users
    response = client.get("/api/v1/admin/users", headers=headers)
    if response.status_code == 200:
        users = response.json()
        print(f"  [OK] Retrieved {len(users)} users.")
    else:
        print(f"  [FAIL] List users failed: {response.status_code} - {response.text}")

    # Create User via Admin
    new_user_email = "created_by_admin@example.com"
    new_user_data = {
        "email": new_user_email,
        "password": "UserPassword123!",
        "full_name": "Created By Admin"
    }
    response = client.post("/api/v1/admin/users", headers=headers, json=new_user_data)
    if response.status_code == 200:
        created_user = response.json()
        print(f"  [OK] User created by admin: {created_user['email']}")
        created_user_id = created_user['id']
    elif response.status_code == 400 and "already exists" in response.text:
        print("  [INFO] User created by admin already exists.")
        # Fetch ID to continue test
        # We can find it in the list we just fetched if we want, or just skip
        # Let's try to find it in the list
        created_user_id = None
        for u in users:
            if u['email'] == new_user_email:
                created_user_id = u['id']
                break
    else:
        print(f"  [FAIL] Create user by admin failed: {response.status_code} - {response.text}")
        created_user_id = None

    # Update User
    if created_user_id:
        update_data = {"full_name": "Updated By Admin"}
        response = client.put(f"/api/v1/admin/users/{created_user_id}", headers=headers, json=update_data)
        if response.status_code == 200:
            print("  [OK] User updated by admin.")
        else:
            print(f"  [FAIL] Update user failed: {response.status_code}")

        # Reset Password
        response = client.post(f"/api/v1/admin/users/{created_user_id}/reset-password", headers=headers, params={"new_password": "NewPassword123!"})
        if response.status_code == 200:
            print("  [OK] User password reset by admin.")
        else:
            print(f"  [FAIL] Password reset failed: {response.status_code}")

    # 5. Test Transaction Management
    print("\n4. Testing Admin Transaction Management...")
    response = client.get("/api/v1/admin/transactions", headers=headers)
    if response.status_code == 200:
        transactions = response.json()
        print(f"  [OK] Retrieved {len(transactions)} transactions.")
        if transactions:
            trans_id = transactions[0]['id']
            # Get Single Transaction
            response = client.get(f"/api/v1/admin/transactions/{trans_id}", headers=headers)
            if response.status_code == 200:
                 print(f"  [OK] Retrieved single transaction: {trans_id}")
            else:
                 print(f"  [FAIL] Get single transaction failed: {response.status_code}")
    else:
        print(f"  [FAIL] List transactions failed: {response.status_code}")

if __name__ == "__main__":
    verify_admin_flow()
