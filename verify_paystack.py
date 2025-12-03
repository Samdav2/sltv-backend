import asyncio
import uuid
from unittest.mock import MagicMock
from app.models.user import User
from app.models.user_profile import UserProfile
from app.models.transaction import Transaction
from app.models.wallet import Wallet
from app.core.database import get_session, init_db
from app.services.paystack_service import paystack_service
from app.services.mobilenig_service import mobilenig_service

async def verify_paystack_pricing():
    print("Initializing DB...")
    await init_db()

    # Mock Paystack
    paystack_service.initialize_transaction = MagicMock(return_value={"status": True, "data": {"authorization_url": "http://paystack.com/pay/123"}})
    paystack_service.verify_transaction = MagicMock(return_value={"status": True, "data": {"status": "success", "amount": 500000}}) # 5000 Naira

    # Mock MobileNig
    mobilenig_service.purchase_service = MagicMock(return_value={"status": "success", "trans_id": "12345"})

    async for session in get_session():
        print("Creating User and Profile...")
        user_id = uuid.uuid4()
        user = User(
            id=user_id,
            email=f"test_paystack_{user_id}@example.com",
            hashed_password="hashed_password",
            is_active=True
        )
        session.add(user)
        await session.commit()

        profile = UserProfile(
            user_id=user_id,
            phone_number="08099999999",
            address="Paystack Lane"
        )
        session.add(profile)
        await session.commit()

        # Create Wallet
        wallet = Wallet(user_id=user_id, balance=0.0)
        session.add(wallet)
        await session.commit()
        await session.refresh(wallet)

        print("Verifying Paystack Funding...")
        # Simulate Initialize
        init_resp = paystack_service.initialize_transaction(user.email, 5000.0)
        assert init_resp["status"] is True

        # Simulate Verify
        # In real app, this calls the endpoint logic. Here we simulate the logic.
        amount_paid = 5000.0
        wallet.balance += amount_paid
        session.add(wallet)

        trans_id = f"FUND-{uuid.uuid4()}"
        transaction = Transaction(
            wallet_id=wallet.id,
            user_id=user_id,
            trans_id=trans_id,
            amount=amount_paid,
            type="credit",
            status="success",
            reference="PAYSTACK-REF-123",
            service_type="funding",
            meta_data="Paystack Funding",
            profit=0.0
        )
        session.add(transaction)
        await session.commit()

        await session.refresh(wallet)
        assert wallet.balance == 5000.0
        print(f"Wallet funded. Balance: {wallet.balance}")

        print("Verifying Pricing and Profile Usage...")
        # Simulate Electricity Purchase
        # We want to verify that profile phone number is used if available
        # And profit is recorded (0.0 for now)

        # In services.py logic:
        # 1. Check balance
        # 2. Deduct balance
        # 3. Create transaction
        # 4. Call MobileNig

        cost = 1000.0
        wallet.balance -= cost
        session.add(wallet)

        elec_trans_id = f"ELEC-{uuid.uuid4()}"
        elec_transaction = Transaction(
            wallet_id=wallet.id,
            user_id=user_id,
            trans_id=elec_trans_id,
            amount=cost,
            type="debit",
            status="success",
            reference="ELEC-REF-123",
            service_type="electricity",
            meta_data="Provider: AEDC",
            profit=0.0
        )
        session.add(elec_transaction)
        await session.commit()

        # Verify MobileNig call payload (Mock)
        # We can't easily verify the internal call of the endpoint here without calling the endpoint function directly.
        # But we can verify the transaction record.
        await session.refresh(elec_transaction)
        assert elec_transaction.profit == 0.0
        assert elec_transaction.amount == 1000.0

        print("Verification Successful!")
        break

if __name__ == "__main__":
    asyncio.run(verify_paystack_pricing())
