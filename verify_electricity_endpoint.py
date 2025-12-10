import asyncio
from unittest.mock import MagicMock, patch
from app.schemas.service import ElectricityVerifyRequest
from app.models.user import User

# Mock dependencies
async def mock_get_current_active_user():
    user = MagicMock(spec=User)
    user.id = "user_123"
    return user

async def verify_endpoint():
    print("Verifying Electricity Verification Endpoint...")

    # Patch ebills_service in services.py
    with patch("app.api.v1.endpoints.services.ebills_service") as mock_ebills_service:
        # Setup mock return values
        async def async_verify(*args, **kwargs):
            return {
                "code": "success",
                "message": "Customer Details Retrieved",
                "data": {
                    "customer_name": "Test Customer",
                    "meter_number": "12345678901",
                    "address": "Test Address"
                }
            }
        mock_ebills_service.verify_customer.side_effect = async_verify

        # Import the function to test
        from app.api.v1.endpoints.services import verify_electricity

        # Create Request with "eddc" provider
        request = ElectricityVerifyRequest(
            provider="eddc",
            meter_number="12345678901",
            type="prepaid"
        )

        user = await mock_get_current_active_user()

        print("Calling verify_electricity with provider='eddc'...")
        try:
            response = await verify_electricity(
                request=request,
                current_user=user
            )
            print(f"Response: {response}")

            # Verify ebills_service was called
            if mock_ebills_service.verify_customer.called:
                print("SUCCESS: ebills_service.verify_customer was called!")
                print(f"Call args: {mock_ebills_service.verify_customer.call_args}")

                # Verify response structure
                assert response["status"] == "success"
                assert response["data"]["customer_name"] == "Test Customer"
                print("Response verification passed!")
            else:
                print("FAILURE: ebills_service.verify_customer was NOT called.")
                exit(1)

        except Exception as e:
            print(f"Error: {e}")
            exit(1)

if __name__ == "__main__":
    asyncio.run(verify_endpoint())
