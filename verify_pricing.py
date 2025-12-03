import asyncio
import uuid
from unittest.mock import MagicMock
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.transaction import Transaction
from app.models.wallet import Wallet
from app.models.service_price import ServicePrice, ProfitType
from app.core.database import get_session, init_db
from app.services.mobilenig_service import mobilenig_service
from app.schemas.service import AirtimeRequest

async def verify_pricing_userdata():
    print("Initializing DB...")
    await init_db()

    # Mock MobileNig
    mobilenig_service.purchase_service = MagicMock(return_value={"status": "success", "trans_id": "12345"})

    async for session in get_session():
        print("Creating User and Profile...")
        user_id = uuid.uuid4()
        user = User(
            id=user_id,
            email=f"test_pricing_{user_id}@example.com",
            hashed_password="hashed_password",
            is_active=True,
            full_name="Test User"
        )
        session.add(user)

        profile = UserProfile(
            user_id=user_id,
            phone_number="08011111111",
            address="Pricing Blvd"
        )
        session.add(profile)

        # Create Wallet
        wallet = Wallet(user_id=user_id, balance=1000.0)
        session.add(wallet)

        # Create Service Price
        # Check if exists first
        from sqlmodel import select
        statement = select(ServicePrice).where(ServicePrice.service_identifier == "airtime-mtn")
        result = await session.exec(statement)
        existing = result.first()

        if not existing:
            service_price = ServicePrice(
                service_identifier="airtime-mtn",
                profit_type=ProfitType.FIXED,
                profit_value=10.0
            )
            session.add(service_price)

        await session.commit()
        await session.refresh(user) # Load profile

        print("Verifying Airtime Purchase with Pricing...")
        # Request amount is Cost Price (e.g. 100.0)
        # Selling Price should be 100.0 + 10.0 = 110.0

        from app.api.v1.endpoints.services import purchase_airtime

        # We need to mock dependencies
        # But calling the function directly requires mocking Depends which is hard.
        # Instead, we will simulate the logic or use a test client.
        # Using test client is better but requires full app setup.
        # Let's simulate the logic flow by calling the function with manual arguments.

        # Mock Wallet Repo
        wallet_repo = MagicMock()

        # Create an awaitable future for the wallet return value
        future_wallet = asyncio.Future()
        future_wallet.set_result(wallet)
        wallet_repo.get_by_user_id = MagicMock(return_value=future_wallet)

        # update and create_transaction are also awaited
        future_none = asyncio.Future()
        future_none.set_result(None)
        wallet_repo.update = MagicMock(return_value=future_none)
        wallet_repo.create_transaction = MagicMock(return_value=future_none)
        wallet_repo.update_transaction = MagicMock(return_value=future_none)

        # We need to pass the session to the function now

        request = AirtimeRequest(phone_number="08022222222", amount=100.0, network="MTN")

        # Call the function
        # Note: purchase_airtime is async
        try:
            await purchase_airtime(
                request=request,
                background_tasks=MagicMock(),
                current_user=user,
                wallet_repo=wallet_repo,
                session=session
            )
        except Exception as e:
            print(f"Error during purchase: {e}")
            raise e

        print("Verifying Wallet Deduction...")
        # Wallet balance should be 1000.0 - 110.0 = 890.0
        # Since we mocked wallet_repo.update, the wallet object in memory might be updated if the function modified it in place.
        # The function does: wallet.balance -= selling_price
        assert wallet.balance == 890.0
        print(f"Wallet balance correct: {wallet.balance}")

        print("Verifying Transaction Profit...")
        # Check the transaction object passed to create_transaction
        call_args = wallet_repo.create_transaction.call_args
        transaction = call_args[0][0]
        assert transaction.profit == 10.0
        assert transaction.amount == 110.0
        print(f"Transaction profit correct: {transaction.profit}")

        print("Verifying User Data Injection...")
        # Check mobilenig_service.purchase_service call args
        call_args = mobilenig_service.purchase_service.call_args
        payload = call_args[0][0]

        assert payload["email"] == user.email
        assert payload["customerName"] == user.full_name
        assert payload["address"] == profile.address
        assert payload["amount"] == 100.0 # Cost price sent to provider
        print("User data injected correctly.")

        print("Verification Successful!")
        break

if __name__ == "__main__":
    asyncio.run(verify_pricing_userdata())
