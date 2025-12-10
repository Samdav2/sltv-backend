import asyncio
from unittest.mock import MagicMock, patch
from app.services.ebills_service import EBillsService

async def verify_ebills_integration():
    print("Starting eBills Integration Verification...")

    # Mock settings
    with patch("app.services.ebills_service.settings") as mock_settings:
        mock_settings.EBILLS_BASE_URL = "https://mock-ebills.africa"
        mock_settings.EBILLS_USERNAME = "mock_user"
        mock_settings.EBILLS_PASSWORD = "mock_password"

        service = EBillsService()

        # Mock httpx.AsyncClient
        with patch("httpx.AsyncClient") as mock_client_cls:
            mock_client = MagicMock()
            mock_client_cls.return_value.__aenter__.return_value = mock_client

            # 1. Test Authentication
            print("\n1. Testing Authentication...")
            mock_auth_response = MagicMock()
            mock_auth_response.status_code = 200
            mock_auth_response.json.return_value = {
                "token": "mock_jwt_token",
                "user_email": "mock@email.com"
            }

            # Fix: Make client.post return an awaitable
            async def async_post(*args, **kwargs):
                return mock_auth_response
            mock_client.post.side_effect = async_post

            token = await service._get_token()
            print(f"Token received: {token}")
            assert token == "mock_jwt_token"
            print("Authentication Test Passed!")

            # 2. Test Verify Customer
            print("\n2. Testing Verify Customer...")
            mock_verify_response = MagicMock()
            mock_verify_response.status_code = 200
            mock_verify_response.json.return_value = {
                "code": "success",
                "message": "Customer Details Retrieved",
                "data": {
                    "customer_name": "Test Customer",
                    "meter_number": "12345678901"
                }
            }

            # Fix: Make client.request return an awaitable
            async def async_request(*args, **kwargs):
                # Return different responses based on endpoint if needed,
                # but here we just update the return value before call or use side_effect logic
                return mock_verify_response

            mock_client.request.side_effect = async_request

            verify_result = await service.verify_customer("12345678901", "enugu-electric")
            print(f"Verify Result: {verify_result}")
            assert verify_result["code"] == "success"
            print("Verify Customer Test Passed!")

            # 3. Test Purchase Electricity
            print("\n3. Testing Purchase Electricity...")
            mock_purchase_response = MagicMock()
            mock_purchase_response.status_code = 200
            mock_purchase_response.json.return_value = {
                "code": "success",
                "message": "ORDER COMPLETED",
                "data": {
                    "order_id": 12345,
                    "status": "completed-api",
                    "token": "1234-5678-9012-3456"
                }
            }

            # Update the return value for the next call
            async def async_request_purchase(*args, **kwargs):
                return mock_purchase_response
            mock_client.request.side_effect = async_request_purchase

            purchase_result = await service.purchase_electricity(
                "req_123", "12345678901", "enugu-electric", "prepaid", 1000
            )
            print(f"Purchase Result: {purchase_result}")
            assert purchase_result["code"] == "success"
            assert purchase_result["data"]["token"] == "1234-5678-9012-3456"
            print("Purchase Electricity Test Passed!")

if __name__ == "__main__":
    asyncio.run(verify_ebills_integration())
