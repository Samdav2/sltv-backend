import requests
from typing import Optional, Dict, Any
from app.core.config import settings

class PaystackService:
    def __init__(self):
        self.base_url = settings.PAYSTACK_BASE_URL
        self.secret_key = settings.PAYSTACK_SECRET_KEY
        self.headers = {
            "Authorization": f"Bearer {self.secret_key}",
            "Content-Type": "application/json"
        }

    def initialize_transaction(self, email: str, amount: float, callback_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Initialize a Paystack transaction.
        Amount should be in Naira (will be converted to Kobo).
        """
        url = f"{self.base_url}/transaction/initialize"
        # Paystack expects amount in kobo
        amount_kobo = int(amount * 100)

        payload = {
            "email": email,
            "amount": amount_kobo,
        }
        if callback_url:
            payload["callback_url"] = callback_url

        response = requests.post(url, headers=self.headers, json=payload)
        response.raise_for_status()
        return response.json()

    def verify_transaction(self, reference: str) -> Dict[str, Any]:
        """
        Verify a Paystack transaction.
        """
        url = f"{self.base_url}/transaction/verify/{reference}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()
        return response.json()

paystack_service = PaystackService()
