from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from fastapi.concurrency import run_in_threadpool
from app.api import deps
from app.models.user import User
from app.schemas.service import AirtimeRequest, DataRequest, ElectricityRequest, ElectricityVerifyRequest, TVRequest, TVRefreshRequest
from app.models.transaction import Transaction
from app.repositories.wallet_repository import WalletRepository
from app.services.automation_service import VTUAutomator
from app.services.mobilenig_service import mobilenig_service
from app.services.vtpass_service import vtpass_service
from app.services.ebills_service import ebills_service
from app.services.email_service import EmailService
from app.models.service_price import ServicePrice, ProfitType
from sqlmodel import select

from datetime import datetime
import logging
import random
import string

logger = logging.getLogger(__name__)

router = APIRouter()

async def _handle_service_failure(
    *,
    transaction: Transaction,
    wallet,
    wallet_repo: WalletRepository,
    background_tasks: BackgroundTasks,
    current_user: User,
    service_name: str,
    amount: float,
    reference: str,
    error: Exception | str,
) -> None:
    error_text = str(error)
    transaction.status = "failed"
    transaction.meta_data += f" | Error: {error_text}"
    await wallet_repo.update_transaction(transaction)

    EmailService.send_purchase_failed_email(
        background_tasks,
        current_user.email,
        current_user.full_name,
        service_name,
        amount,
        reference,
        error_text,
    )

    wallet.balance += amount
    await wallet_repo.update(wallet, {"balance": wallet.balance})

    refund_trans_id = generate_trans_id("REFUND")
    refund_transaction = Transaction(
        wallet_id=wallet.id,
        user_id=current_user.id,
        trans_id=refund_trans_id,
        amount=amount,
        type="credit",
        status="success",
        reference=f"REFUND-{transaction.id}",
        service_type="refund",
        meta_data=f"Refund for failed {service_name} transaction {transaction.id}",
        profit=0.0,
    )
    await wallet_repo.create_transaction(refund_transaction)

    EmailService.send_refund_email(
        background_tasks,
        current_user.email,
        current_user.full_name,
        service_name,
        amount,
        refund_transaction.reference,
    )


def should_refund_on_failure(transaction: Transaction) -> bool:
    """Only refund when the purchase never reached a successful terminal state."""
    return transaction.status != "success"


async def _finalize_service_success(
    *,
    transaction: Transaction,
    wallet_repo: WalletRepository,
    background_tasks: BackgroundTasks,
    current_user: User,
    service_name: str,
    amount: float,
    reference: str,
    recipient: str,
    result_message: str,
) -> None:
    transaction.status = "success"
    transaction.meta_data += f" | Result: {result_message}"
    await wallet_repo.update_transaction(transaction)

    try:
        EmailService.send_purchase_success_email(
            background_tasks,
            current_user.email,
            current_user.full_name,
            service_name,
            amount,
            reference,
            recipient,
        )
    except Exception as email_error:
        logger.exception("Purchase success email notification failed")
        transaction.meta_data += f" | Notification Warning: {email_error}"
        await wallet_repo.update_transaction(transaction)


def generate_trans_id(prefix: str) -> str:
    """Generates a unique transaction ID <= 15 chars for MobileNig compatibility"""
    # MobileNig limit is 15 chars.
    # Format: YYMMDDHHMMSS (12) + 3 random chars = 15 chars
    timestamp = datetime.now().strftime("%y%m%d%H%M%S")
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3))
    return f"{timestamp}{suffix}"

def process_airtime_purchase(request: AirtimeRequest, transaction_id: int, wallet_repo: WalletRepository):
    # This should ideally be in a separate service method that handles DB session
    # For now, we are using the global automator
    vtu_automator = VTUAutomator()
    success = vtu_automator.purchase_airtime(request)
    # Here we would update the transaction status
    # Since we don't have a fresh session here easily without more boilerplate,
    # we'll assume this part is handled by a proper worker in production.
    # For this MVP, we just log.
    if success:
        print(f"Transaction {transaction_id} completed successfully.")
    else:
        print(f"Transaction {transaction_id} failed.")

@router.post("/airtime")
async def purchase_airtime(
    request: AirtimeRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user),
    wallet_repo: WalletRepository = Depends(deps.get_wallet_repository),
    session: deps.AsyncSession = Depends(deps.get_session),
):
    """
    Purchase airtime.
    """
    # 1. Calculate Price
    service_identifier = f"airtime-{request.network.lower()}" # e.g. airtime-mtn
    statement = select(ServicePrice).where(ServicePrice.service_identifier == service_identifier)
    result = await session.exec(statement)
    price_config = result.first()

    cost_price = request.amount
    profit = 0.0

    if price_config:
        if price_config.profit_type == ProfitType.FIXED:
            profit = price_config.profit_value
        elif price_config.profit_type == ProfitType.PERCENTAGE:
            profit = cost_price * (price_config.profit_value / 100)

    selling_price = cost_price + profit

    wallet = await wallet_repo.get_by_user_id(current_user.id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    if wallet.balance < selling_price:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # Deduct balance
    wallet.balance -= selling_price
    await wallet_repo.update(wallet, {"balance": wallet.balance})

    # Create transaction
    trans_id = generate_trans_id("AIRTIME")

    transaction = Transaction(
        wallet_id=wallet.id,
        user_id=current_user.id,
        trans_id=trans_id,
        amount=selling_price, # User pays selling price
        type="debit",
        status="processing",
        reference=f"AIRTIME-{wallet.id}-{request.phone_number}",
        service_type="airtime",
        meta_data=f"Network: {request.network}",
        profit=profit
    )
    await wallet_repo.create_transaction(transaction)

    # Execute immediately for now as MobileNig is fast API
    try:
        payload = {
            "service_id": request.network,
            "phoneNumber": request.phone_number,
            "amount": cost_price, # Service provider gets cost price
            "trans_id": trans_id,
            # User Data Injection
            "email": current_user.email,
            "customerName": current_user.full_name or "",
            "address": current_user.profile.address if current_user.profile else ""
        }
        response = await mobilenig_service.purchase_service(payload)
        await _finalize_service_success(
            transaction=transaction,
            wallet_repo=wallet_repo,
            background_tasks=background_tasks,
            current_user=current_user,
            service_name=f"Airtime {request.network} {request.amount}",
            amount=selling_price,
            reference=transaction.reference,
            recipient=request.phone_number,
            result_message=str(response),
        )

    except Exception as e:
        logger.exception("Airtime purchase failed")
        if should_refund_on_failure(transaction):
            await _handle_service_failure(
                transaction=transaction,
                wallet=wallet,
                wallet_repo=wallet_repo,
                background_tasks=background_tasks,
                current_user=current_user,
                service_name=f"Airtime {request.network} {request.amount}",
                amount=selling_price,
                reference=transaction.reference,
                error=e,
            )
        else:
            transaction.meta_data += f" | Post-success error: {e}"
            await wallet_repo.update_transaction(transaction)

    return {"message": "Airtime purchase processing", "transaction_id": transaction.id}

@router.post("/data")
async def purchase_data(
    request: DataRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user),
    wallet_repo: WalletRepository = Depends(deps.get_wallet_repository),
    session: deps.AsyncSession = Depends(deps.get_session),
):
    """
    Purchase data.
    """
    # 1. Calculate Price
    service_identifier = f"data-{request.network.lower()}" # e.g. data-mtn
    statement = select(ServicePrice).where(ServicePrice.service_identifier == service_identifier)
    result = await session.exec(statement)
    price_config = result.first()

    cost_price = request.amount
    profit = 0.0

    if price_config:
        if price_config.profit_type == ProfitType.FIXED:
            profit = price_config.profit_value
        elif price_config.profit_type == ProfitType.PERCENTAGE:
            profit = cost_price * (price_config.profit_value / 100)

    selling_price = cost_price + profit

    wallet = await wallet_repo.get_by_user_id(current_user.id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    if wallet.balance < selling_price:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # Deduct balance
    wallet.balance -= selling_price
    await wallet_repo.update(wallet, {"balance": wallet.balance})

    trans_id = generate_trans_id("DATA")

    transaction = Transaction(
        wallet_id=wallet.id,
        user_id=current_user.id,
        trans_id=trans_id,
        amount=selling_price,
        type="debit",
        status="processing",
        reference=f"DATA-{wallet.id}-{request.phone_number}",
        service_type="data",
        meta_data=f"Plan: {request.plan_id}",
        profit=profit
    )
    await wallet_repo.create_transaction(transaction)

    try:
        payload = {
            "service_id": request.plan_id, # Assuming plan_id is the service_id
            "phoneNumber": request.phone_number,
            "trans_id": trans_id,
            # User Data Injection
            "email": current_user.email,
            "customerName": current_user.full_name or "",
            "address": current_user.profile.address if current_user.profile else ""
        }
        response = await mobilenig_service.purchase_service(payload)
        await _finalize_service_success(
            transaction=transaction,
            wallet_repo=wallet_repo,
            background_tasks=background_tasks,
            current_user=current_user,
            service_name=f"Data {request.network} {request.plan_id}",
            amount=selling_price,
            reference=transaction.reference,
            recipient=request.phone_number,
            result_message=str(response),
        )

    except Exception as e:
        logger.exception("Data purchase failed")
        if should_refund_on_failure(transaction):
            await _handle_service_failure(
                transaction=transaction,
                wallet=wallet,
                wallet_repo=wallet_repo,
                background_tasks=background_tasks,
                current_user=current_user,
                service_name=f"Data {request.network} {request.plan_id}",
                amount=selling_price,
                reference=transaction.reference,
                error=e,
            )
        else:
            transaction.meta_data += f" | Post-success error: {e}"
            await wallet_repo.update_transaction(transaction)

    return {"message": "Data purchase processing", "transaction_id": transaction.id}

def process_electricity_purchase(request: ElectricityRequest, transaction_id: int, wallet_repo: WalletRepository):
    vtu_automator = VTUAutomator()
    success = vtu_automator.purchase_electricity(request)
    if success:
        print(f"Transaction {transaction_id} completed successfully.")
    else:
        print(f"Transaction {transaction_id} failed.")

@router.post("/electricity/verify")
async def verify_electricity(
    request: ElectricityVerifyRequest,
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Verify electricity customer details.
    """
    try:
        # Map provider aliases
        service_id = request.provider
        if request.provider.lower() in ["enugu-electric", "eedc", "eddc"]:
            service_id = "enugu-electric"

        # eBills Integration for EEDC (and potentially others if migrated)
        if service_id == "enugu-electric":
             # Map request type to eBills variation
            variation_id = "prepaid"
            if request.type.lower() == "postpaid":
                variation_id = "postpaid"

            verify_resp = await ebills_service.verify_customer(
                customer_id=request.meter_number,
                service_id=service_id,
                variation_id=variation_id
            )

            if verify_resp.get("code") == "success":
                return {"status": "success", "data": verify_resp.get("data")}
            else:
                 raise HTTPException(status_code=400, detail=f"Verification Failed: {verify_resp.get('message')}")

        # Fallback to MobileNig or other logic if needed for other providers
        # For now, we only explicitly handle EEDC via eBills as requested.
        # If we want to support others, we'd need to check MobileNig verification support or similar.
        # Assuming MobileNig doesn't have a direct "verify" endpoint exposed here easily without more work,
        # we might just return a generic "Verification not supported for this provider yet" or mock it.

        return {"status": "success", "message": "Verification skipped for this provider (not fully implemented yet).", "data": {"customer_name": "Verified User"}}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/electricity")
async def purchase_electricity(
    request: ElectricityRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user),
    wallet_repo: WalletRepository = Depends(deps.get_wallet_repository),
    session: deps.AsyncSession = Depends(deps.get_session),
):
    """
    Purchase electricity.
    """
    # 1. Calculate Price
    service_identifier = f"electricity-{request.provider.lower()}" # e.g. electricity-aedc
    statement = select(ServicePrice).where(ServicePrice.service_identifier == service_identifier)
    result = await session.exec(statement)
    price_config = result.first()

    cost_price = request.amount
    profit = 0.0

    if price_config:
        if price_config.profit_type == ProfitType.FIXED:
            profit = price_config.profit_value
        elif price_config.profit_type == ProfitType.PERCENTAGE:
            profit = cost_price * (price_config.profit_value / 100)

    selling_price = cost_price + profit

    wallet = await wallet_repo.get_by_user_id(current_user.id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    if wallet.balance < selling_price:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # Deduct balance
    wallet.balance -= selling_price
    await wallet_repo.update(wallet, {"balance": wallet.balance})

    trans_id = generate_trans_id("ELEC")

    # Use profile data if request data is missing (optional logic, but user asked for it)
    # Example: if phone number is needed for notification and not in request.
    # ElectricityRequest has meter_number.
    # MobileNig purchase might need phone number.
    # Let's check payload construction.

    transaction = Transaction(
        wallet_id=wallet.id,
        user_id=current_user.id,
        trans_id=trans_id,
        amount=selling_price,
        type="debit",
        status="processing",
        reference=f"ELEC-{wallet.id}-{request.meter_number}",
        service_type="electricity",
        meta_data=f"Provider: {request.provider}, Type: {request.type}",
        profit=profit
    )
    await wallet_repo.create_transaction(transaction)

    try:
        # Use user profile phone number if available
        phone_number = "08000000000" # Default
        if current_user.profile and current_user.profile.phone_number:
            phone_number = current_user.profile.phone_number

        # CHECK PROVIDER FOR ROUTING
        # If provider is EEDC (Enugu Electric), route to eBills Africa
        if request.provider.lower() in ["enugu-electric", "eedc", "eddc"]:
            # eBills Africa Integration

            # Map request type to eBills variation (prepaid/postpaid)
            variation_id = "prepaid"
            if request.type.lower() == "postpaid":
                variation_id = "postpaid"

            # Verify Customer first (Optional but good practice, though purchase might fail if invalid)
            # For now, let's go straight to purchase to match previous flow speed,
            # or we can verify if we want to be sure.
            # The user documentation says "Verify the customer first using /api/v2/verify-customer".
            # Let's try to verify first.

            try:
                verify_resp = await ebills_service.verify_customer(
                    customer_id=request.meter_number,
                    service_id="enugu-electric",
                    variation_id=variation_id
                )
                if verify_resp.get("code") != "success":
                     raise Exception(f"Customer Verification Failed: {verify_resp.get('message')}")
            except Exception as verify_err:
                 # If verification fails, we should probably stop and error out
                 raise Exception(f"Verification Error: {str(verify_err)}")

            response = await ebills_service.purchase_electricity(
                request_id=trans_id,
                customer_id=request.meter_number,
                service_id="enugu-electric",
                variation_id=variation_id,
                amount=cost_price
            )

            # Check eBills response code
            if response.get("code") == "success":
                data = response.get("data", {})
                token = data.get("token")
                success_note = f"eBills Response: {response}"
                if token:
                    success_note += f" | Token: {token}"

                await _finalize_service_success(
                    transaction=transaction,
                    wallet_repo=wallet_repo,
                    background_tasks=background_tasks,
                    current_user=current_user,
                    service_name=f"Electricity {request.provider} {request.amount}",
                    amount=selling_price,
                    reference=transaction.reference,
                    recipient=f"{request.meter_number} (Token: {token})" if token else request.meter_number,
                    result_message=success_note,
                )
            else:
                raise Exception(f"eBills Error: {response.get('message', 'Unknown error')}")

        else:
            # MobileNig Integration (Default for others)
            payload = {
                "service_id": request.provider, # Assuming provider is service_id (e.g. AEDC)
                "meterNumber": request.meter_number, # Correct field name per error
                "amount": cost_price,
                "trans_id": trans_id,
                "phoneNumber": phone_number,
                "customerDtNumber": "0000", # Default or dummy if not available
                "customerAddress": current_user.profile.address if current_user.profile and current_user.profile.address else "Nigeria",
                "customerAccountType": request.type.upper(), # PREPAID or POSTPAID
                "contactType": "LANDLORD", # Default value
                # User Data Injection
                "email": current_user.email,
                "customerName": current_user.full_name or "",
                "address": current_user.profile.address if current_user.profile else ""
            }
            response = await mobilenig_service.purchase_service(payload)
            await _finalize_service_success(
                transaction=transaction,
                wallet_repo=wallet_repo,
                background_tasks=background_tasks,
                current_user=current_user,
                service_name=f"Electricity {request.provider} {request.amount}",
                amount=selling_price,
                reference=transaction.reference,
                recipient=request.meter_number,
                result_message=str(response),
            )

    except Exception as e:
        logger.exception("Electricity purchase failed")
        if should_refund_on_failure(transaction):
            await _handle_service_failure(
                transaction=transaction,
                wallet=wallet,
                wallet_repo=wallet_repo,
                background_tasks=background_tasks,
                current_user=current_user,
                service_name=f"Electricity {request.provider} {request.amount}",
                amount=selling_price,
                reference=transaction.reference,
                error=e,
            )
        else:
            transaction.meta_data += f" | Post-success error: {e}"
            await wallet_repo.update_transaction(transaction)

    return {"message": "Electricity purchase processing", "transaction_id": transaction.id}

def process_tv_purchase(request: TVRequest, transaction_id: int, wallet_repo: WalletRepository):
    vtu_service = VTUAutomator()
    success = vtu_service.purchase_tv(request)
    if success:
        print(f"Transaction {transaction_id} completed successfully.")
    else:
        print(f"Transaction {transaction_id} failed.")

@router.post("/tv/details")
async def get_tv_details(
    request: TVRequest,
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Get TV user details (specifically for SLTV).
    Uses local automation service.
    """
    def run_automation():
        vtu_service = VTUAutomator()
        return vtu_service.get_sltv_user_details(request)

    try:
        details = await run_in_threadpool(run_automation)
        if details is False:
            raise HTTPException(status_code=400, detail="Could not retrieve user details")
        return details
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Local Automation Error: {str(e)}")

@router.post("/tv/refresh")
async def refresh_tv(
    request: TVRefreshRequest,
    current_user: User = Depends(deps.get_current_active_user),
):
    """
    Refresh TV subscription (specifically for SLTV).
    Uses local automation service.
    """
    def run_automation():
        vtu_service = VTUAutomator()
        return vtu_service.refresh_tv(request)

    try:
        result = await run_in_threadpool(run_automation)
        if result is False:
            raise HTTPException(status_code=400, detail="Refresh failed")
        return {"status": "success", "message": result}
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Local Automation Error: {str(e)}")

@router.post("/tv")
async def purchase_tv(
    request: TVRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user),
    wallet_repo: WalletRepository = Depends(deps.get_wallet_repository),
):
    """
    Purchase TV subscription (e.g. SLTV).
    Uses Local Automation Service.
    """
    # 1. Check Balance
    wallet = await wallet_repo.get_by_user_id(current_user.id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    if wallet.balance < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # 2. Deduct Balance immediately
    wallet.balance -= request.amount
    await wallet_repo.update(wallet, {"balance": wallet.balance})

    trans_id = generate_trans_id("TV")
    transaction = Transaction(
        wallet_id=wallet.id,
        user_id=current_user.id,
        trans_id=trans_id,
        amount=request.amount,
        type="debit",
        status="processing",
        reference=f"TV-{wallet.id}-{request.smart_card_number}",
        service_type="tv",
        meta_data=f"Provider: {request.provider}",
        profit=0.0
    )
    await wallet_repo.create_transaction(transaction)

    def run_automation():
        vtu_service = VTUAutomator()
        return vtu_service.purchase_tv(request)

    try:
        result_message = await run_in_threadpool(run_automation)

        if result_message is not False:
            await _finalize_service_success(
                transaction=transaction,
                wallet_repo=wallet_repo,
                background_tasks=background_tasks,
                current_user=current_user,
                service_name=f"TV {request.provider} {request.amount}",
                amount=request.amount,
                reference=transaction.reference,
                recipient=request.smart_card_number,
                result_message=str(result_message),
            )

            return {"status": "success", "message": result_message, "transaction_id": transaction.id}
        else:
            raise Exception("Local Automation returned False (failed)")

    except Exception as e:
        logger.exception("TV purchase failed")
        if should_refund_on_failure(transaction):
            await _handle_service_failure(
                transaction=transaction,
                wallet=wallet,
                wallet_repo=wallet_repo,
                background_tasks=background_tasks,
                current_user=current_user,
                service_name=f"TV {request.provider} {request.amount}",
                amount=request.amount,
                reference=transaction.reference,
                error=e,
            )
        else:
            transaction.meta_data += f" | Post-success error: {e}"
            await wallet_repo.update_transaction(transaction)

        raise HTTPException(
            status_code=502,
            detail=str(e),
        )

    return {"status": "processing", "message": "TV purchase processing", "transaction_id": transaction.id}
