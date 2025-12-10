import asyncio
from unittest.mock import MagicMock, patch
from app.api.v1.endpoints.enugu_electricity import EnuguElectricityVerifyRequest, EnuguElectricityPurchaseRequest
from app.models.user import User
from app.models.wallet import Wallet

# Mock dependencies
async def mock_get_current_active_user():
    user = MagicMock(spec=User)
    user.id = "user_123"
    user.email = "test@example.com"
    user.full_name = "Test User"
    return user

async def mock_get_wallet_repo():
    repo = MagicMock()
    wallet = MagicMock(spec=Wallet)
    wallet.id = "wallet_123"
    wallet.balance = 5000.0

    async def async_get(*args, **kwargs):
        return wallet
    repo.get_by_user_id.side_effect = async_get

    async def async_update(*args, **kwargs):
        return None
    repo.update.side_effect = async_update
    repo.create_transaction.side_effect = async_update
    repo.update_transaction.side_effect = async_update

    return repo

async def verify_enugu_endpoints():
    print("Verifying Enugu Electricity Endpoints...")

    with patch("app.api.v1.endpoints.enugu_electricity.ebills_service") as mock_ebills_service:
        # Mock Verify
        async def async_verify(*args, **kwargs):
            return {
                "code": "success",
                "message": "Customer Details Retrieved",
                "data": {"customer_name": "Test Customer"}
            }
        mock_ebills_service.verify_customer.side_effect = async_verify

        # Mock Purchase
        async def async_purchase(*args, **kwargs):
            return {
                "code": "success",
                "message": "Purchase Successful",
                "data": {"token": "TOKEN-123"}
            }
        mock_ebills_service.purchase_electricity.side_effect = async_purchase

        from app.api.v1.endpoints.enugu_electricity import verify_enugu_electricity, purchase_enugu_electricity

        user = await mock_get_current_active_user()
        wallet_repo = await mock_get_wallet_repo()
        background_tasks = MagicMock()

        # 1. Test Verify
        print("\nTesting Verify Endpoint...")
        verify_req = EnuguElectricityVerifyRequest(meter_number="12345", type="prepaid")
        verify_resp = await verify_enugu_electricity(verify_req, user)
        print(f"Verify Response: {verify_resp}")
        assert verify_resp["status"] == "success"
        assert mock_ebills_service.verify_customer.called
        print("Verify Endpoint Passed!")

        # 2. Test Purchase
        print("\nTesting Purchase Endpoint...")
        purchase_req = EnuguElectricityPurchaseRequest(meter_number="12345", amount=100.0, type="prepaid")
        purchase_resp = await purchase_enugu_electricity(
            purchase_req, background_tasks, user, wallet_repo
        )
        print(f"Purchase Response: {purchase_resp}")
        assert purchase_resp["status"] == "success"
        assert mock_ebills_service.purchase_electricity.called
        print("Purchase Endpoint Passed!")

if __name__ == "__main__":
    asyncio.run(verify_enugu_endpoints())
