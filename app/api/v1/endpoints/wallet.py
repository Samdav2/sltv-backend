import uuid
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from app.api import deps
from app.models.user import User
from app.schemas.wallet import WalletRead
from app.schemas.transaction import TransactionRead
from app.models.transaction import Transaction
from app.repositories.wallet_repository import WalletRepository

from app.repositories.wallet_repository import WalletRepository
from datetime import datetime
import random
import string

from app.services.paystack_service import paystack_service
from app.core.config import settings

router = APIRouter()

def generate_trans_id(prefix: str) -> str:
    """Generates a unique transaction ID <= 15 chars"""
    # Format: YYMMDDHHMMSS (12) + 3 random chars = 15 chars
    timestamp = datetime.now().strftime("%y%m%d%H%M%S")
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    return f"{timestamp}{suffix}"

@router.get("/me", response_model=WalletRead)
async def get_my_wallet(
    current_user: User = Depends(deps.get_current_active_user),
    wallet_repo: WalletRepository = Depends(deps.get_wallet_repository),
) -> Any:
    """
    Get current user's wallet.
    """
    wallet = await wallet_repo.get_by_user_id(current_user.id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

@router.post("/fund", response_model=TransactionRead)
async def fund_wallet(
    amount: float,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user),
    wallet_repo: WalletRepository = Depends(deps.get_wallet_repository),
) -> Any:
    """
    Fund wallet (Mock implementation).
    """
    wallet = await wallet_repo.get_by_user_id(current_user.id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    # Create transaction
    trans_id = generate_trans_id("FUND")
    transaction = Transaction(
        wallet_id=wallet.id,
        user_id=current_user.id,
        trans_id=trans_id,
        amount=amount,
        type="credit",
        status="success",
        reference=f"FUND-{wallet.id}-{amount}",
        service_type="funding",
        meta_data="Manual funding"
    )
    await wallet_repo.create_transaction(transaction)

    # Update wallet balance
    wallet.balance += amount
    await wallet_repo.update(wallet, {"balance": wallet.balance})

    # Send Wallet Funded Email
    from app.services.email_service import EmailService
    EmailService.send_wallet_funded_email(
        background_tasks,
        current_user.email,
        current_user.full_name,
        amount,
        wallet.balance,
        transaction.reference
    )

    return transaction

@router.get("/{wallet_id}/transactions", response_model=List[TransactionRead])
async def get_transactions(
    wallet_id: uuid.UUID,
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
    wallet_repo: deps.WalletRepository = Depends(deps.get_wallet_repository),
) -> Any:
    """
    Get transaction history.
    """
    wallet = await wallet_repo.get_by_user_id(current_user.id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    transactions = await wallet_repo.get_transactions(wallet.id, skip=skip, limit=limit)
    return transactions

@router.post("/fund/paystack/initialize")
async def initialize_paystack_funding(
    amount: float,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Initialize Paystack funding transaction.
    """
    try:
        response = paystack_service.initialize_transaction(
            email=current_user.email,
            amount=amount
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/fund/paystack/verify")
async def verify_paystack_funding(
    reference: str,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user),
    wallet_repo: WalletRepository = Depends(deps.get_wallet_repository),
) -> Any:
    """
    Verify Paystack funding transaction and credit wallet.
    """
    try:
        verification = paystack_service.verify_transaction(reference)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Verification failed: {str(e)}")

    if verification["status"] and verification["data"]["status"] == "success":
        amount_paid = verification["data"]["amount"] / 100 # Convert kobo to Naira

        wallet = await wallet_repo.get_by_user_id(current_user.id)
        if not wallet:
             raise HTTPException(status_code=404, detail="Wallet not found")

        trans_id = generate_trans_id("FUND")
        transaction = Transaction(
            wallet_id=wallet.id,
            user_id=current_user.id,
            trans_id=trans_id,
            amount=amount_paid,
            type="credit",
            status="success",
            reference=reference,
            service_type="funding",
            meta_data="Paystack Funding",
            profit=0.0
        )

        await wallet_repo.create_transaction(transaction)

        wallet.balance += amount_paid
        await wallet_repo.update(wallet, {"balance": wallet.balance})

        # Send Wallet Funded Email
        from app.services.email_service import EmailService
        EmailService.send_wallet_funded_email(
            background_tasks,
            current_user.email,
            current_user.full_name,
            amount_paid,
            wallet.balance,
            reference
        )

        return {"status": "success", "message": "Wallet funded successfully", "amount": amount_paid}
    else:
        raise HTTPException(status_code=400, detail="Payment verification failed")
