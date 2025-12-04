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

# Add project root to path
sys.path.append(os.getcwd())

from app.main import app
from app.core.config import settings
from app.models.user import User

client = TestClient(app)

def verify_support_flow():
    print("Verifying Support Flow...")

    # User Credentials
    user_email = "support_user@example.com"
    user_password = "UserPassword123!"

    # Admin Credentials (reusing from admin test)
    admin_email = "admin_test@example.com"
    admin_password = "AdminPassword123!"

    # 1. Register User
    print("\n1. Registering User...")
    register_data = {
        "email": user_email,
        "password": user_password,
        "full_name": "Support User"
    }
    client.post("/api/v1/users/", json=register_data) # Ignore error if exists

    # 2. Login User
    print("\n2. Logging in User...")
    login_data = {"username": user_email, "password": user_password}
    response = client.post("/api/v1/auth/login/access-token", data=login_data)
    if response.status_code != 200:
        print(f"  [FAIL] User login failed: {response.status_code}")
        return
    user_token = response.json()["access_token"]
    user_headers = {"Authorization": f"Bearer {user_token}"}
    print("  [OK] User logged in.")

    # 3. Create Ticket
    print("\n3. Creating Ticket...")
    ticket_data = {
        "subject": "Issue with Payment",
        "priority": "high",
        "message": "I cannot fund my wallet."
    }
    response = client.post("/api/v1/support/", headers=user_headers, json=ticket_data)
    if response.status_code == 200:
        ticket = response.json()
        ticket_id = ticket["id"]
        print(f"  [OK] Ticket created: #{ticket_id}")
    else:
        print(f"  [FAIL] Create ticket failed: {response.status_code} - {response.text}")
        return

    # 4. Login Admin
    print("\n4. Logging in Admin...")
    login_data = {"username": admin_email, "password": admin_password}
    response = client.post("/api/v1/auth/login/access-token", data=login_data)
    if response.status_code != 200:
        print(f"  [FAIL] Admin login failed: {response.status_code}")
        return
    admin_token = response.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    print("  [OK] Admin logged in.")

    # 5. Admin List Tickets
    print("\n5. Admin Listing Tickets...")
    response = client.get("/api/v1/admin/support/tickets", headers=admin_headers)
    if response.status_code == 200:
        tickets = response.json()
        print(f"  [OK] Admin sees {len(tickets)} tickets.")
        found = any(t["id"] == ticket_id for t in tickets)
        if found:
            print("  [OK] Created ticket found in admin list.")
        else:
            print("  [FAIL] Created ticket NOT found in admin list.")
    else:
        print(f"  [FAIL] Admin list tickets failed: {response.status_code}")

    # 6. Admin Reply
    print("\n6. Admin Replying...")
    reply_data = {"message": "We are checking this issue."}
    response = client.post(f"/api/v1/support/{ticket_id}/message", headers=admin_headers, json=reply_data)
    if response.status_code == 200:
        print("  [OK] Admin replied.")
    else:
        print(f"  [FAIL] Admin reply failed: {response.status_code} - {response.text}")

    # 7. User Check Reply
    print("\n7. User Checking Reply...")
    response = client.get(f"/api/v1/support/{ticket_id}", headers=user_headers)
    if response.status_code == 200:
        ticket_details = response.json()
        messages = ticket_details["messages"]
        print(f"  [OK] Ticket has {len(messages)} messages.")
        if len(messages) >= 2:
            last_msg = messages[-1]
            if last_msg["is_admin"]:
                print("  [OK] Last message is from Admin.")
            else:
                print("  [FAIL] Last message is NOT from Admin.")
        else:
            print("  [FAIL] Reply not found.")
    else:
        print(f"  [FAIL] User get ticket failed: {response.status_code}")

if __name__ == "__main__":
    verify_support_flow()
