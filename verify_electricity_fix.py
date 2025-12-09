import asyncio
from unittest.mock import MagicMock, patch, AsyncMock
from app.api.v1.endpoints.services import purchase_electricity
from app.schemas.service import ElectricityRequest
from app.models.user import User
from app.models.user_profile import UserProfile
from app.repositories.wallet_repository import WalletRepository
from app.models.wallet import Wallet

async def verify_electricity_payload():
    print("Verifying Electricity Purchase Payload Construction...")

    # Mock dependencies
    mock_background_tasks = MagicMock()

    mock_user = User(
        id="12345678-1234-5678-1234-567812345678",
        email="test@example.com",
        hashed_password="hash",
        full_name="Test User"
    )
    mock_user.profile = UserProfile(
        user_id=mock_user.id,
        address="123 Test St, Lagos",
        phone_number="08012345678"
    )

    mock_wallet = Wallet(id="wallet-123", user_id=mock_user.id, balance=5000.0)

    mock_wallet_repo = MagicMock(spec=WalletRepository)
    mock_wallet_repo.get_by_user_id = AsyncMock(return_value=mock_wallet)
    mock_wallet_repo.update = AsyncMock(return_value=None)
    mock_wallet_repo.create_transaction = AsyncMock(return_value=None)
    mock_wallet_repo.update_transaction = AsyncMock(return_value=None)

    mock_session = MagicMock()
    # Mock exec to be awaitable
    async def mock_exec(*args, **kwargs):
        mock_result = MagicMock()
        mock_result.first.return_value = None
        return mock_result
    mock_session.exec = mock_exec

    # Request data
    request = ElectricityRequest(
        meter_number="111222333",
        amount=1000.0,
        provider="AEDC",
        type="prepaid"
    )

    # Patch mobilenig_service to capture the payload
    with patch("app.services.mobilenig_service.mobilenig_service.purchase_service", new_callable=MagicMock) as mock_purchase:
        # Make the return value awaitable
        future = asyncio.Future()
        future.set_result({"status": "success", "message": "Purchased"})
        mock_purchase.return_value = future

        try:
            await purchase_electricity(
                request=request,
                background_tasks=mock_background_tasks,
                current_user=mock_user,
                wallet_repo=mock_wallet_repo,
                session=mock_session
            )

            # Verify payload
            mock_purchase.assert_called_once()
            call_args = mock_purchase.call_args[0][0]

            print("\nCaptured Payload:")
            import json
            print(json.dumps(call_args, indent=2))

            required_fields = ["meterNumber", "customerDtNumber", "customerAddress", "customerAccountType", "contactType"]
            missing = [f for f in required_fields if f not in call_args]

            if not missing:
                print("\n✅ All required fields are present.")
                if call_args["customerAccountType"] == "PREPAID":
                    print("✅ customerAccountType is correct (PREPAID).")
                else:
                    print(f"❌ customerAccountType is incorrect: {call_args['customerAccountType']}")
            else:
                print(f"\n❌ Missing fields: {missing}")

        except Exception as e:
            print(f"\n❌ Error during execution: {e}")

if __name__ == "__main__":
    asyncio.run(verify_electricity_payload())
