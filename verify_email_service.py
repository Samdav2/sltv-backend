import os
import sys
from unittest.mock import MagicMock
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Set mock credentials if missing to pass Settings validation
if not os.getenv("MAIL_JET_API"):
    os.environ["MAIL_JET_API"] = "mock_api_key"
if not os.getenv("MAIL_JET_SECRET"):
    os.environ["MAIL_JET_SECRET"] = "mock_secret_key"
if not os.getenv("MAIL_FROM"):
    os.environ["MAIL_FROM"] = "test@example.com"

# Add the project root to the python path
sys.path.append(os.getcwd())

from app.services.email_service import EmailService, mailjet, template_env
from app.core.config import settings

def verify_email_service():
    print("Verifying Email Service...")

    target_email = "adoxop1@gmail.com"
    print(f"Target Email: {target_email}")

    # 1. Verify Template Loading
    print("\n1. Verifying Template Loading...")
    templates = [
        "user_welcome.html",
        "email_verification.html",
        "email_verified_notice.html",
        "password_reset.html",
        "password_change_notice.html",
        "email_change_notice.html",
        "wallet_funded.html",
        "purchase_success.html",
        "purchase_failed.html",
        "refund_processed.html"
    ]

    for template_name in templates:
        try:
            template = template_env.get_template(template_name)
            print(f"  [OK] Template found: {template_name}")
        except Exception as e:
            print(f"  [FAIL] Template not found: {template_name} - {e}")

    # 2. Verify Template Rendering
    print("\n2. Verifying Template Rendering (Sample)...")
    try:
        context = {"name": "Test User"}
        rendered = EmailService._render_template("user_welcome.html", context)
        if "Test User" in rendered and "Welcome to SLTV VTU!" in rendered:
            print("  [OK] user_welcome.html rendered correctly with new branding.")
        else:
            print("  [FAIL] user_welcome.html rendering failed content check.")
    except Exception as e:
        print(f"  [FAIL] Rendering error: {e}")

    # 3. Verify Send Logic
    print("\n3. Verifying Send Logic...")

    # Check if we have real credentials
    if settings.MAIL_JET_API and settings.MAIL_JET_SECRET and settings.MAIL_FROM:
        print("  [INFO] Real Mailjet credentials found. Attempting to send REAL email...")
        # We do NOT mock mailjet.send here
    else:
        print("  [INFO] No Mailjet credentials found. Using MOCK...")
        # Mock the mailjet client's send.create method
        mailjet.send = MagicMock()
        mailjet.send.create.return_value.status_code = 200

    try:
        EmailService._send_email_async(
            subject="System Verification Test",
            email_to=target_email,
            template_body={"name": "Verifier"},
            template_name="user_welcome.html"
        )

        if settings.MAIL_JET_API and settings.MAIL_JET_SECRET and settings.MAIL_FROM:
             print(f"  [DONE] Real email send attempted to {target_email}. Check inbox.")
        else:
            # Check if called correctly (Mocked)
            if mailjet.send.create.called:
                print("  [OK] mailjet.send.create was called (Mocked).")
                args, kwargs = mailjet.send.create.call_args
                data = kwargs['data']
                if data['Messages'][0]['To'][0]['Email'] == target_email:
                     print("  [OK] Recipient email matches.")
                if data['Messages'][0]['From']['Name'] == "SLTV VTU":
                     print("  [OK] Sender name matches 'SLTV VTU'.")
            else:
                print("  [FAIL] mailjet.send.create was NOT called.")

    except Exception as e:
        print(f"  [FAIL] Send logic error: {e}")

    # 4. Verify New Methods (Mocked for safety, or Real if desired - let's keep mocked for bulk/transactional to avoid spamming unless requested)
    # For this verification, we will just test the Welcome email with real credentials if available.
    # We can test one VTU method as well.

    print("\n4. Verifying Wallet Funded Email...")
    try:
        EmailService.send_wallet_funded_email(
            MagicMock(), # BackgroundTasks mock
            target_email,
            "Verifier",
            5000.0,
            10000.0,
            "REF_VERIFY_123"
        )
        print("  [OK] send_wallet_funded_email called successfully (Task added).")
        # Note: Since we passed a mock BackgroundTasks, it won't actually execute the send function
        # unless we manually execute it or use a real BackgroundTasks object (which needs an event loop).
        # For this script, we are mainly testing the method signature and task addition.

    except Exception as e:
        print(f"  [FAIL] send_wallet_funded_email error: {e}")

if __name__ == "__main__":
    verify_email_service()
