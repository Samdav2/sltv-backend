import logging
from typing import Optional

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        pass

    async def send_verification_email(self, email: str, token: str):
        # Mock email sending
        logger.info(f"Sending verification email to {email} with token: {token}")
        print(f"----- EMAIL SIMULATION -----\nTo: {email}\nSubject: Verify your email\nBody: Use this token to verify your account: {token}\n----------------------------")
        return True

    async def send_password_reset_email(self, email: str, token: str):
        # Mock email sending
        logger.info(f"Sending password reset email to {email} with token: {token}")
        print(f"----- EMAIL SIMULATION -----\nTo: {email}\nSubject: Reset your password\nBody: Use this token to reset your password: {token}\n----------------------------")
        return True

email_service = EmailService()
