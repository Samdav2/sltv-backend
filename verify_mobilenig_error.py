import asyncio
from unittest.mock import MagicMock, patch
from app.services.mobilenig_service import MobileNigService

async def test_mobilenig_failure():
    service = MobileNigService()

    # Mock response data for a failure case
    failure_response = {
        "status": "success", # The HTTP request itself is successful
        "message": "failure",
        "statusCode": "EXC006",
        "details": "Service is currently unavailable."
    }

    print("Testing MobileNig failure response handling...")

    with patch("httpx.AsyncClient.request") as mock_request:
        mock_response = MagicMock()
        mock_response.json.return_value = failure_response
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response

        try:
            # We can call any method that uses _make_request, e.g., get_balance
            # The arguments don't matter much since we are mocking the response
            await service.get_balance()
            print("❌ Test Failed: Exception was NOT raised for failure response.")
        except Exception as e:
            print(f"✅ Test Passed: Exception caught as expected.")
            print(f"   Error message: {e}")
            if "Service is currently unavailable" in str(e):
                 print("   ✅ Error message contains expected details.")
            else:
                 print("   ❌ Error message does NOT contain expected details.")

if __name__ == "__main__":
    asyncio.run(test_mobilenig_failure())
