import httpx
import logging
from typing import Optional, Any, Dict
from app.core.config import settings
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)

class EBillsService:
    def __init__(self):
        self.base_url = settings.EBILLS_BASE_URL
        self.username = settings.EBILLS_USERNAME
        self.password = settings.EBILLS_PASSWORD
        self.token = None
        self.token_expiry = None

    async def _get_token(self) -> str:
        """
        Get a valid JWT token. Authenticates if token is missing or expired.
        """
        if self.token and self.token_expiry and datetime.now() < self.token_expiry:
            return self.token

        url = f"{self.base_url}/jwt-auth/v1/token"
        payload = {
            "username": self.username,
            "password": self.password
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, timeout=30.0)
                response_data = response.json()

                if response.status_code == 200 and "token" in response_data:
                    self.token = response_data["token"]
                    # Token expires in 7 days, but let's refresh it sooner to be safe (e.g., 6 days)
                    self.token_expiry = datetime.now() + timedelta(days=6)
                    return self.token
                else:
                    logger.error(f"eBills Auth Failed: {response_data}")
                    raise Exception(f"Authentication failed: {response_data.get('message', 'Unknown error')}")
            except httpx.RequestError as e:
                raise Exception(f"Auth Request failed: {str(e)}")

    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None, auth_required: bool = True) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        headers = {
            "Content-Type": "application/json"
        }

        if auth_required:
            token = await self._get_token()
            headers["Authorization"] = f"Bearer {token}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(method, url, headers=headers, json=data, timeout=60.0)
                response_data = response.json()

                # Log raw response for debugging
                logger.info(f"eBills Response ({endpoint}): {response_data}")

                # eBills might return 200 with error code in body, or 4xx/5xx
                # Check for "code" in response body if it exists, or rely on status code

                if response.status_code >= 400:
                     raise Exception(f"HTTP Error {response.status_code}: {response.text}")

                return response_data
            except httpx.RequestError as e:
                raise Exception(f"Request failed: {str(e)}")

    async def verify_customer(self, customer_id: str, service_id: str, variation_id: str = "prepaid") -> Dict[str, Any]:
        """
        Verify Customer Details (e.g. Meter Number).
        """
        payload = {
            "customer_id": customer_id,
            "service_id": service_id,
            "variation_id": variation_id
        }
        return await self._make_request("POST", "/api/v2/verify-customer", data=payload)

    async def purchase_electricity(self,
                                   request_id: str,
                                   customer_id: str,
                                   service_id: str,
                                   variation_id: str,
                                   amount: float) -> Dict[str, Any]:
        """
        Purchase Electricity.
        """
        payload = {
            "request_id": request_id,
            "customer_id": customer_id,
            "service_id": service_id,
            "variation_id": variation_id,
            "amount": amount
        }
        return await self._make_request("POST", "/api/v2/electricity", data=payload)

    async def requery_order(self, request_id: str) -> Dict[str, Any]:
        """
        Requery Order Status.
        """
        payload = {
            "request_id": request_id
        }
        return await self._make_request("POST", "/api/v2/requery", data=payload)

ebills_service = EBillsService()
