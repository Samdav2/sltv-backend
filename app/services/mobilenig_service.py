import requests
import json
import logging
from typing import Optional, Any, Dict
from app.core.config import settings
from app.schemas.mobilenig import (
    BalanceResponse,
    ServicesStatusResponse,
    CustomerValidationResponse,
    PurchaseResponse,
    QueryTransactionResponse,
)

logger = logging.getLogger(__name__)

class MobileNigService:
    def __init__(self):
        self.base_url = settings.MOBILENIG_BASE_URL
        self.public_key = settings.MOBILENIG_PUBLIC_KEY
        self.secret_key = settings.MOBILENIG_SECRET_KEY
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.public_key}"
        }
        self.secret_headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.secret_key}"
        }

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, use_secret_key: bool = False) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        headers = self.secret_headers if use_secret_key else self.headers

        try:
            response = requests.request(method, url, headers=headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # In a real app, you'd want better error handling/logging here
            if response is not None:
                try:
                    error_data = response.json()
                    raise Exception(f"MobileNig API Error: {error_data}")
                except ValueError:
                    pass
            raise Exception(f"Request failed: {str(e)}")

    def get_balance(self) -> BalanceResponse:
        """Check wallet balance."""
        data = self._make_request("GET", "/control/balance")
        return BalanceResponse(**data)

    def get_services_status(self, service_id: str = "All") -> ServicesStatusResponse:
        """Get status of services."""
        params = f"?service_id={service_id}"
        data = self._make_request("GET", f"/control/services_status{params}", use_secret_key=False)
        # Wait, the Postman collection shows 'Bearer {{public_live_key}}' for services status.
        # And 'Bearer {{public_key}}' for balance.
        # I'll stick to public key for 'read' ops usually, but let's see.
        # Actually, let's use public key.
        return ServicesStatusResponse(**data)

    def validate_customer(self, service_id: str, customer_account_id: str) -> CustomerValidationResponse:
        """Validate a customer (SmartCard, Meter No, etc.)."""
        payload = {
            "service_id": service_id,
            "customerAccountId": customer_account_id
        }
        data = self._make_request("POST", "/services/proxy", data=payload)
        logger.info(f"DEBUG: validate_customer raw response: {data}")
        return CustomerValidationResponse(**data)

    def purchase_service(self, payload: Dict[str, Any]) -> PurchaseResponse:
        """Purchase a service (Airtime, Data, etc.)."""
        # Purchases usually require the secret key
        if "trans_id" not in payload:
            import uuid
            payload["trans_id"] = uuid.uuid4().hex[:12] # MobileNig might have length limits, using 12 chars is usually safe or check docs. User example was "3293902390" (10 digits). Let's use 12 random digits or hex.
            # Actually user example "3293902390" looks like numeric. Let's use numeric string if possible or just hex.
            # Let's use a random numeric string to be safe if they expect numbers.
            # But standard is often unique string. I'll stick to uuid hex for uniqueness unless specified.
            # Re-reading: "trans_id": "3293902390".
            # I will use a numeric string generator just in case.
            import random
            import string
            payload["trans_id"] = ''.join(random.choices(string.digits, k=15))

        data = self._make_request("POST", "/services/", data=payload, use_secret_key=True)
        return PurchaseResponse(**data)

    def query_transaction(self, trans_id: str) -> QueryTransactionResponse:
        """Query the status of a transaction."""
        params = f"?trans_id={trans_id}"
        data = self._make_request("GET", f"/services/query{params}", use_secret_key=True)
        return QueryTransactionResponse(**data)

mobilenig_service = MobileNigService()
