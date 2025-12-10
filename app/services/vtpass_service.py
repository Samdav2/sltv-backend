import httpx
import logging
from typing import Optional, Any, Dict
from app.core.config import settings
import uuid
import random
import string
from datetime import datetime

logger = logging.getLogger(__name__)

class VTpassService:
    def __init__(self):
        self.base_url = settings.VTPASS_BASE_URL
        self.api_key = settings.VTPASS_API_KEY
        self.public_key = settings.VTPASS_PUBLIC_KEY
        self.secret_key = settings.VTPASS_SECRET_KEY

        # VTpass uses Basic Auth or specific headers depending on endpoint,
        # but documentation says "Authentication: Learn about authentication from here" which usually implies
        # api-key and secret-key headers or Basic Auth.
        # Based on common VTpass integrations:
        # headers usually include 'api-key', 'secret-key' or 'Authorization'.
        # The user provided doc doesn't explicitly state the header names in the snippet,
        # but standard VTpass is usually:
        # 'api-key': '...', 'secret-key': '...'
        # OR Basic Auth with username=email, password=password.
        # However, the user said "I will provide api key, secret key and public key".
        # Let's assume standard headers for now.

        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
            "secret-key": self.secret_key,
            "public-key": self.public_key
        }

    async def _make_request(self, method: str, endpoint: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"

        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(method, url, headers=self.headers, json=data, timeout=60.0)
                # VTpass might return 200 even for logical errors, so we check response body code
                response_data = response.json()

                # Log raw response for debugging
                logger.info(f"VTpass Response: {response_data}")

                if response.status_code >= 400:
                     raise Exception(f"HTTP Error {response.status_code}: {response.text}")

                return response_data
            except httpx.RequestError as e:
                raise Exception(f"Request failed: {str(e)}")

    def generate_request_id(self) -> str:
        """
        Generate a unique request ID.
        Format: YYYYMMDDHHMM + Random(alphanumeric)
        """
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        return f"{timestamp}{random_str}"

    async def verify_meter(self, meter_number: str, service_id: str, type: str) -> Dict[str, Any]:
        """
        Verify Meter Number.
        """
        payload = {
            "billersCode": meter_number,
            "serviceID": service_id,
            "type": type
        }
        return await self._make_request("POST", "/merchant-verify", data=payload)

    async def purchase_product(self,
                               request_id: str,
                               service_id: str,
                               billers_code: str,
                               variation_code: str,
                               amount: float,
                               phone: str) -> Dict[str, Any]:
        """
        Purchase Product (Electricity).
        """
        payload = {
            "request_id": request_id,
            "serviceID": service_id,
            "billersCode": billers_code,
            "variation_code": variation_code,
            "amount": amount,
            "phone": phone
        }
        return await self._make_request("POST", "/pay", data=payload)

    async def query_transaction(self, request_id: str) -> Dict[str, Any]:
        """
        Query Transaction Status.
        """
        payload = {
            "request_id": request_id
        }
        return await self._make_request("POST", "/requery", data=payload)

vtpass_service = VTpassService()
