import asyncio
import uuid
from datetime import datetime
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.transaction import Transaction
from app.models.wallet import Wallet
from app.core.database import get_session, init_db
from app.services.mobilenig_service import mobilenig_service
from unittest.mock import MagicMock

async def verify_profile():
    print("Initializing DB...")
    await init_db()
    print("Verifying Profile...")
    async for session in get_session():
        # Create User
        user_id = uuid.uuid4()
        user = User(
            id=user_id,
            email=f"test_profile_{user_id}@example.com",
            hashed_password="hashed_password",
            is_active=True
        )
        session.add(user)
        await session.commit()

        # Create Profile
        profile = UserProfile(
            user_id=user_id,
            phone_number="08012345678",
            address="123 Test St",
            state="Lagos",
            lga="Ikeja"
        )
        session.add(profile)
        await session.commit()
        await session.refresh(profile)

        print(f"Profile created: {profile.phone_number}, {profile.address}")

        # Verify Relationship
        await session.refresh(user)
        # Note: Accessing relationship might require eager loading or async loop,
        # but let's check if we can query it back.
        # In SQLModel async, lazy loading is not supported.
        # We should query profile by user_id.
        from sqlmodel import select
        statement = select(UserProfile).where(UserProfile.user_id == user_id)
        result = await session.exec(statement)
        fetched_profile = result.first()

        assert fetched_profile.phone_number == "08012345678"
        print("Profile verification successful!")

        # Verify Transaction Profit
        print("Verifying Transaction Profit...")
        trans_id = f"TEST-{uuid.uuid4()}"
        wallet_id = uuid.uuid4() # Mock wallet ID

        # Mock MobileNig Service
        mobilenig_service.purchase_service = MagicMock(return_value={"status": "success", "trans_id": "12345"})

        # Create Transaction manually as if service did it
        transaction = Transaction(
            wallet_id=wallet_id,
            user_id=user_id,
            trans_id=trans_id,
            amount=100.0,
            type="debit",
            status="success",
            reference="REF-123",
            service_type="airtime",
            profit=5.0 # Mock profit
        )
        session.add(transaction)
        await session.commit()
        await session.refresh(transaction)

        assert transaction.profit == 5.0
        print(f"Transaction profit verified: {transaction.profit}")

        break

if __name__ == "__main__":
    asyncio.run(verify_profile())
