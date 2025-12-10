from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from app.api import deps
from app.models.user import User
from app.models.transaction import Transaction
from app.repositories.wallet_repository import WalletRepository
from app.services.ebills_service import ebills_service
from app.services.email_service import EmailService
from sqlmodel import SQLModel
from datetime import datetime
import random
import string

router = APIRouter()

class EnuguElectricityVerifyRequest(SQLModel):
    meter_number: str
    type: str = "prepaid" # prepaid or postpaid

class EnuguElectricityPurchaseRequest(SQLModel):
    meter_number: str
    amount: float
    admin_amount: float
    type: str = "prepaid"

def generate_trans_id(prefix: str) -> str:
    """Generates a unique transaction ID"""
    timestamp = datetime.now().strftime("%y%m%d%H%M%S")
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    return f"{timestamp}{suffix}"

@router.post("/verify")
async def verify_enugu_electricity(
    request: EnuguElectricityVerifyRequest,
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Verify Enugu Electricity (EEDC) customer details.
    """
    try:
        variation_id = "prepaid"
        if request.type.lower() == "postpaid":
            variation_id = "postpaid"

        verify_resp = await ebills_service.verify_customer(
            customer_id=request.meter_number,
            service_id="enugu-electric",
            variation_id=variation_id
        )

        if verify_resp.get("code") == "success":
            return {"status": "success", "data": verify_resp.get("data")}
        else:
             raise HTTPException(status_code=400, detail=f"Verification Failed: {verify_resp.get('message')}")

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/purchase")
async def purchase_enugu_electricity(
    request: EnuguElectricityPurchaseRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user),
    wallet_repo: WalletRepository = Depends(deps.get_wallet_repository),
):
    """
    Purchase Enugu Electricity (EEDC).
    """
    # 1. Check Wallet Balance
    wallet = await wallet_repo.get_by_user_id(current_user.id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    if wallet.balance < request.admin_amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # 2. Deduct Balance (Admin Amount)
    wallet.balance -= request.admin_amount
    await wallet_repo.update(wallet, {"balance": wallet.balance})

    # 3. Create Transaction
    trans_id = generate_trans_id("EEDC")
    transaction = Transaction(
        wallet_id=wallet.id,
        user_id=current_user.id,
        trans_id=trans_id,
        amount=request.admin_amount, # Record admin amount as transaction amount
        type="debit",
        status="processing",
        reference=f"EEDC-{wallet.id}-{request.meter_number}",
        service_type="electricity",
        meta_data=f"Provider: Enugu Electric (EEDC), Type: {request.type}, Cost: {request.amount}",
        profit=request.admin_amount - request.amount
    )
    await wallet_repo.create_transaction(transaction)

    try:
        # 4. Call eBills Service (Use Cost Price / Provider Amount)
        variation_id = "prepaid"
        if request.type.lower() == "postpaid":
            variation_id = "postpaid"

        response = await ebills_service.purchase_electricity(
            request_id=trans_id,
            customer_id=request.meter_number,
            service_id="enugu-electric",
            variation_id=variation_id,
            amount=request.amount # Send actual cost amount to provider
        )

        if response.get("code") == "success":
            transaction.status = "success"
            transaction.meta_data += f" | eBills Response: {response}"

            data = response.get("data", {})
            token = data.get("token")
            if token:
                 transaction.meta_data += f" | Token: {token}"

            await wallet_repo.update_transaction(transaction)

            # Send Success Email
            EmailService.send_purchase_success_email(
                background_tasks,
                current_user.email,
                current_user.full_name,
                f"Electricity EEDC {request.amount}",
                request.admin_amount,
                transaction.reference,
                f"{request.meter_number} (Token: {token})" if token else request.meter_number
            )

            return {"status": "success", "message": "Purchase successful", "data": data, "transaction_id": transaction.id}
        else:
            raise Exception(f"eBills Error: {response.get('message', 'Unknown error')}")

    except Exception as e:
        # 5. Handle Failure & Refund
        transaction.status = "failed"
        transaction.meta_data += f" | Error: {str(e)}"
        await wallet_repo.update_transaction(transaction)

        # Send Failed Email
        EmailService.send_purchase_failed_email(
            background_tasks,
            current_user.email,
            current_user.full_name,
            f"Electricity EEDC {request.amount}",
            request.admin_amount,
            transaction.reference,
            str(e)
        )

        # Refund (Admin Amount)
        wallet.balance += request.admin_amount
        await wallet_repo.update(wallet, {"balance": wallet.balance})

        refund_trans_id = generate_trans_id("REFUND")
        refund_transaction = Transaction(
            wallet_id=wallet.id,
            user_id=current_user.id,
            trans_id=refund_trans_id,
            amount=request.admin_amount,
            type="credit",
            status="success",
            reference=f"REFUND-{transaction.id}",
            service_type="refund",
            meta_data=f"Refund for failed EEDC transaction {transaction.id}"
        )
        await wallet_repo.create_transaction(refund_transaction)

        # Send Refund Email
        EmailService.send_refund_email(
            background_tasks,
            current_user.email,
            current_user.full_name,
            f"Electricity EEDC {request.amount}",
            request.admin_amount,
            refund_transaction.reference
        )

        raise HTTPException(status_code=400, detail=f"Transaction failed: {str(e)}")
