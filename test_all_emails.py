"""
Test script to send all email templates to a specified email address.
This tests all 12 EZY VTU email templates.
"""
import asyncio
import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import BackgroundTasks
from app.services.email_service import EmailService

# Test email address
TEST_EMAIL = "adoxop1@gmail.com"
TEST_NAME = "Test User"

class ImmediateBackgroundTasks:
    """A BackgroundTasks that executes tasks immediately instead of in background."""
    def add_task(self, func, *args, **kwargs):
        func(*args, **kwargs)

def send_all_test_emails():
    """Send all 12 email templates to the test email address."""
    bg_tasks = ImmediateBackgroundTasks()

    print(f"📧 Sending all email templates to: {TEST_EMAIL}")
    print("=" * 60)

    # 1. User Welcome Email
    print("1/12 - Sending: User Welcome Email...")
    EmailService.send_user_welcome_email(
        background_tasks=bg_tasks,
        email_to=TEST_EMAIL,
        name=TEST_NAME
    )
    print("     ✓ Sent!")

    # 2. Email Verification
    print("2/12 - Sending: Email Verification...")
    EmailService.send_email_verification(
        background_tasks=bg_tasks,
        email_to=TEST_EMAIL,
        name=TEST_NAME,
        verification_link="https://ezyvtu.com/verify?token=test123456"
    )
    print("     ✓ Sent!")

    # 3. Email Verified Notice
    print("3/12 - Sending: Email Verified Notice...")
    EmailService.send_email_verified_notice(
        background_tasks=bg_tasks,
        email_to=TEST_EMAIL,
        name=TEST_NAME
    )
    print("     ✓ Sent!")

    # 4. Password Reset
    print("4/12 - Sending: Password Reset...")
    EmailService.send_password_reset_email(
        background_tasks=bg_tasks,
        email_to=TEST_EMAIL,
        name=TEST_NAME,
        reset_link="https://ezyvtu.com/reset-password?token=reset123456"
    )
    print("     ✓ Sent!")

    # 5. Password Change Notice
    print("5/12 - Sending: Password Change Notice...")
    EmailService.send_password_change_notice(
        background_tasks=bg_tasks,
        email_to=TEST_EMAIL,
        name=TEST_NAME
    )
    print("     ✓ Sent!")

    # 6. Email Change Notice
    print("6/12 - Sending: Email Change Notice...")
    EmailService.send_email_change_notice(
        background_tasks=bg_tasks,
        email_to=TEST_EMAIL,
        name=TEST_NAME,
        old_email="old_email@example.com"
    )
    print("     ✓ Sent!")

    # 7. Wallet Funded
    print("7/12 - Sending: Wallet Funded...")
    EmailService.send_wallet_funded_email(
        background_tasks=bg_tasks,
        email_to=TEST_EMAIL,
        name=TEST_NAME,
        amount=5000.00,
        new_balance=15000.00,
        transaction_ref="TXN-WF-123456789"
    )
    print("     ✓ Sent!")

    # 8. Purchase Success
    print("8/12 - Sending: Purchase Success...")
    EmailService.send_purchase_success_email(
        background_tasks=bg_tasks,
        email_to=TEST_EMAIL,
        name=TEST_NAME,
        service_name="MTN 2GB Data Bundle",
        amount=1500.00,
        transaction_ref="TXN-PS-123456789",
        recipient="08012345678"
    )
    print("     ✓ Sent!")

    # 9. Purchase Failed
    print("9/12 - Sending: Purchase Failed...")
    EmailService.send_purchase_failed_email(
        background_tasks=bg_tasks,
        email_to=TEST_EMAIL,
        name=TEST_NAME,
        service_name="GOtv Max Subscription",
        amount=4850.00,
        transaction_ref="TXN-PF-123456789",
        reason="Network provider timeout. Please try again."
    )
    print("     ✓ Sent!")

    # 10. Refund Processed
    print("10/12 - Sending: Refund Processed...")
    EmailService.send_refund_email(
        background_tasks=bg_tasks,
        email_to=TEST_EMAIL,
        name=TEST_NAME,
        service_name="Airtel 1GB Data",
        amount=500.00,
        transaction_ref="TXN-RF-123456789"
    )
    print("     ✓ Sent!")

    # 11. Ticket Created
    print("11/12 - Sending: Ticket Created...")
    EmailService.send_ticket_created_email(
        background_tasks=bg_tasks,
        email_to=TEST_EMAIL,
        name=TEST_NAME,
        ticket_id="TCKT-001234",
        subject="Data not received after purchase",
        message_preview="I made a purchase for MTN 2GB data bundle but haven't received the data yet. The transaction reference is TXN-123..."
    )
    print("     ✓ Sent!")

    # 12. Ticket Reply (Admin)
    print("12/12 - Sending: Ticket Reply (Admin)...")
    EmailService.send_ticket_reply_email(
        background_tasks=bg_tasks,
        email_to=TEST_EMAIL,
        name=TEST_NAME,
        ticket_id="TCKT-001234",
        subject="Data not received after purchase",
        reply_message="Thank you for reaching out! We've investigated your issue and the data has now been successfully delivered to your phone number. Please restart your device if you don't see it immediately. Let us know if you need further assistance!",
        is_admin_reply=True
    )
    print("     ✓ Sent!")

    print("=" * 60)
    print(f"✅ All 12 email templates sent to {TEST_EMAIL}")
    print("Please check your inbox (and spam folder) for the test emails.")

if __name__ == "__main__":
    send_all_test_emails()
