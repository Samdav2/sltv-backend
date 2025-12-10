import asyncio
from unittest.mock import MagicMock, patch
from app.schemas.service import ElectricityRequest
from app.models.user import User
from app.models.wallet import Wallet
from app.models.transaction import Transaction

# Mock dependencies
async def mock_get_current_active_user():
    user = MagicMock(spec=User)
    user.id = "user_123"
    user.email = "test@example.com"
    user.full_name = "Test User"
    user.profile = MagicMock()
    user.profile.address = "Test Address"
    user.profile.phone_number = "08012345678"
    return user

async def mock_get_wallet_repo():
    repo = MagicMock()
    wallet = MagicMock(spec=Wallet)
    wallet.id = "wallet_123"
    wallet.balance = 5000.0

    # Async mocks
    async def async_get(*args, **kwargs):
        return wallet
    repo.get_by_user_id.side_effect = async_get

    async def async_update(*args, **kwargs):
        return None
    repo.update.side_effect = async_update
    repo.create_transaction.side_effect = async_update
    repo.update_transaction.side_effect = async_update

    return repo

async def mock_get_session():
    session = MagicMock()
    async def async_exec(*args, **kwargs):
        result = MagicMock()
        result.first.return_value = None # No special price config
        return result
    session.exec.side_effect = async_exec
    return session

async def verify_eedc_fix():
    print("Verifying EEDC Fix...")

    # Patch ebills_service in services.py
    with patch("app.api.v1.endpoints.services.ebills_service") as mock_ebills_service:
        # Setup mock return values
        async def async_verify(*args, **kwargs):
            return {"code": "success", "message": "Verified"}
        mock_ebills_service.verify_customer.side_effect = async_verify

        async def async_purchase(*args, **kwargs):
            return {"code": "success", "data": {"token": "TOKEN-123"}}
        mock_ebills_service.purchase_electricity.side_effect = async_purchase

        # Import the function to test
        from app.api.v1.endpoints.services import purchase_electricity

        # Create Request with "eddc" provider
        request = ElectricityRequest(
            provider="eddc",
            meter_number="12345678901",
            amount=100.0,
            type="prepaid"
        )

        # Mock BackgroundTasks
        background_tasks = MagicMock()

        # Get mocks
        user = await mock_get_current_active_user()
        wallet_repo = await mock_get_wallet_repo()
        session = await mock_get_session()

        print("Calling purchase_electricity with provider='eddc'...")
        try:
            response = await purchase_electricity(
                request=request,
                background_tasks=background_tasks,
                current_user=user,
                wallet_repo=wallet_repo,
                session=session
            )
            print(f"Response: {response}")

            # Verify ebills_service was called
            if mock_ebills_service.purchase_electricity.called:
                print("SUCCESS: ebills_service.purchase_electricity was called!")
                print(f"Call args: {mock_ebills_service.purchase_electricity.call_args}")
            else:
                print("FAILURE: ebills_service.purchase_electricity was NOT called.")
                exit(1)

        except Exception as e:
            print(f"Error: {e}")
            exit(1)

if __name__ == "__main__":
    asyncio.run(verify_eedc_fix())
