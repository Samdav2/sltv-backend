import httpx
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

    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, use_secret_key: bool = False) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        headers = self.secret_headers if use_secret_key else self.headers

        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(method, url, headers=headers, json=data, timeout=30.0)
                response.raise_for_status()
                response_data = response.json()

                # Check for API-level failure
                if response_data.get("message") == "failure":
                    error_details = response_data.get("details", "Unknown error")
                    raise Exception(f"{error_details}")

                return response_data
            except httpx.HTTPStatusError as e:
                # In a real app, you'd want better error handling/logging here
                if e.response is not None:
                    try:
                        error_data = e.response.json()
                        raise Exception(f"{error_data}")
                    except ValueError:
                        pass
                raise Exception(f"Request failed: {str(e)}")
            except httpx.RequestError as e:
                raise Exception(f"Request failed: {str(e)}")

    async def get_balance(self) -> BalanceResponse:
        """Check wallet balance."""
        data = await self._make_request("GET", "/control/balance")
        return BalanceResponse(**data)

    async def get_services_status(self, service_id: str = "All") -> ServicesStatusResponse:
        """Get status of services."""
        params = f"?service_id={service_id}"
        data = await self._make_request("GET", f"/control/services_status{params}", use_secret_key=False)
        return ServicesStatusResponse(**data)

    async def validate_customer(self, service_id: str, customer_account_id: str) -> CustomerValidationResponse:
        """Validate a customer (SmartCard, Meter No, etc.)."""
        payload = {
            "service_id": service_id,
            "customerAccountId": customer_account_id
        }
        data = await self._make_request("POST", "/services/proxy", data=payload)
        logger.info(f"DEBUG: validate_customer raw response: {data}")
        return CustomerValidationResponse(**data)

    async def purchase_service(self, payload: Dict[str, Any]) -> PurchaseResponse:
        """Purchase a service (Airtime, Data, etc.)."""
        # Purchases usually require the secret key
        if "trans_id" not in payload:
            import uuid
            payload["trans_id"] = uuid.uuid4().hex[:12]
            import random
            import string
            payload["trans_id"] = ''.join(random.choices(string.digits, k=15))

        data = await self._make_request("POST", "/services/", data=payload, use_secret_key=True)
        return PurchaseResponse(**data)

    async def query_transaction(self, trans_id: str) -> QueryTransactionResponse:
        """Query the status of a transaction."""
        params = f"?trans_id={trans_id}"
        data = await self._make_request("GET", f"/services/query{params}", use_secret_key=True)
        return QueryTransactionResponse(**data)

mobilenig_service = MobileNigService()
