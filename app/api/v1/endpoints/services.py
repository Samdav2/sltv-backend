from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.concurrency import run_in_threadpool
from app.api import deps
from app.models.user import User
from app.schemas.service import AirtimeRequest, DataRequest, ElectricityRequest, TVRequest
from app.models.transaction import Transaction
from app.repositories.wallet_repository import WalletRepository
from app.services.automation_service import VTUAutomator
from app.services.mobilenig_service import mobilenig_service
from app.models.service_price import ServicePrice, ProfitType
from sqlmodel import select

from datetime import datetime
import random
import string

router = APIRouter()

def generate_trans_id(prefix: str) -> str:
    """Generates a unique transaction ID: PREFIX-YYYYMMDDHHMMSS-RANDOM"""
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix}-{timestamp}-{suffix}"

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
    from app.services.email_service import EmailService
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
        response = mobilenig_service.purchase_service(payload)
        transaction.status = "success"
        transaction.meta_data += f" | Response: {response}"
        await wallet_repo.update_transaction(transaction)

        # Send Success Email
        EmailService.send_purchase_success_email(
            background_tasks,
            current_user.email,
            current_user.full_name,
            f"Airtime {request.network} {request.amount}",
            selling_price,
            transaction.reference,
            request.phone_number
        )

    except Exception as e:
        transaction.status = "failed"
        transaction.meta_data += f" | Error: {str(e)}"
        await wallet_repo.update_transaction(transaction)

        # Send Failed Email
        EmailService.send_purchase_failed_email(
            background_tasks,
            current_user.email,
            current_user.full_name,
            f"Airtime {request.network} {request.amount}",
            selling_price,
            transaction.reference,
            str(e)
        )

        # Refund
        wallet.balance += selling_price
        await wallet_repo.update(wallet, {"balance": wallet.balance})

        refund_trans_id = generate_trans_id("REFUND")
        refund_transaction = Transaction(
            wallet_id=wallet.id,
            user_id=current_user.id,
            trans_id=refund_trans_id,
            amount=selling_price,
            type="credit",
            status="success",
            reference=f"REFUND-{transaction.id}",
            service_type="refund",
            meta_data=f"Refund for failed Airtime transaction {transaction.id}",
            profit=0.0
        )
        await wallet_repo.create_transaction(refund_transaction)

        # Send Refund Email
        EmailService.send_refund_email(
            background_tasks,
            current_user.email,
            current_user.full_name,
            f"Airtime {request.network} {request.amount}",
            selling_price,
            refund_transaction.reference
        )

        raise HTTPException(status_code=400, detail=f"Transaction failed: {str(e)}")

    return {"message": "Airtime purchase successful", "transaction_id": transaction.id}

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

    from app.services.email_service import EmailService
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
        response = mobilenig_service.purchase_service(payload)
        transaction.status = "success"
        transaction.meta_data += f" | Response: {response}"
        await wallet_repo.update_transaction(transaction)

        # Send Success Email
        EmailService.send_purchase_success_email(
            background_tasks,
            current_user.email,
            current_user.full_name,
            f"Data {request.network} {request.plan_id}",
            selling_price,
            transaction.reference,
            request.phone_number
        )

    except Exception as e:
        transaction.status = "failed"
        transaction.meta_data += f" | Error: {str(e)}"
        await wallet_repo.update_transaction(transaction)

        # Send Failed Email
        EmailService.send_purchase_failed_email(
            background_tasks,
            current_user.email,
            current_user.full_name,
            f"Data {request.network} {request.plan_id}",
            selling_price,
            transaction.reference,
            str(e)
        )

        # Refund
        wallet.balance += selling_price
        await wallet_repo.update(wallet, {"balance": wallet.balance})

        refund_trans_id = generate_trans_id("REFUND")
        refund_transaction = Transaction(
            wallet_id=wallet.id,
            user_id=current_user.id,
            trans_id=refund_trans_id,
            amount=selling_price,
            type="credit",
            status="success",
            reference=f"REFUND-{transaction.id}",
            service_type="refund",
            meta_data=f"Refund for failed Data transaction {transaction.id}",
            profit=0.0
        )
        await wallet_repo.create_transaction(refund_transaction)

        # Send Refund Email
        EmailService.send_refund_email(
            background_tasks,
            current_user.email,
            current_user.full_name,
            f"Data {request.network} {request.plan_id}",
            selling_price,
            refund_transaction.reference
        )

        raise HTTPException(status_code=400, detail=f"Transaction failed: {str(e)}")

    return {"message": "Data purchase successful", "transaction_id": transaction.id}

def process_electricity_purchase(request: ElectricityRequest, transaction_id: int, wallet_repo: WalletRepository):
    vtu_automator = VTUAutomator()
    success = vtu_automator.purchase_electricity(request)
    if success:
        print(f"Transaction {transaction_id} completed successfully.")
    else:
        print(f"Transaction {transaction_id} failed.")

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

    from app.services.email_service import EmailService
    try:
        # Use user profile phone number if available
        phone_number = "08000000000" # Default
        if current_user.profile and current_user.profile.phone_number:
            phone_number = current_user.profile.phone_number

        payload = {
            "service_id": request.provider, # Assuming provider is service_id (e.g. AEDC)
            "customerAccountId": request.meter_number,
            "amount": cost_price,
            "trans_id": trans_id,
            "phoneNumber": phone_number, # Added phone number from profile
            # User Data Injection
            "email": current_user.email,
            "customerName": current_user.full_name or "",
            "address": current_user.profile.address if current_user.profile else ""
        }
        response = mobilenig_service.purchase_service(payload)
        transaction.status = "success"
        transaction.meta_data += f" | Response: {response}"
        await wallet_repo.update_transaction(transaction)

        # Send Success Email
        EmailService.send_purchase_success_email(
            background_tasks,
            current_user.email,
            current_user.full_name,
            f"Electricity {request.provider} {request.amount}",
            selling_price,
            transaction.reference,
            request.meter_number
        )

    except Exception as e:
        transaction.status = "failed"
        transaction.meta_data += f" | Error: {str(e)}"
        await wallet_repo.update_transaction(transaction)

        # Send Failed Email
        EmailService.send_purchase_failed_email(
            background_tasks,
            current_user.email,
            current_user.full_name,
            f"Electricity {request.provider} {request.amount}",
            selling_price,
            transaction.reference,
            str(e)
        )

        # Refund
        wallet.balance += selling_price
        await wallet_repo.update(wallet, {"balance": wallet.balance})

        refund_trans_id = generate_trans_id("REFUND")
        refund_transaction = Transaction(
            wallet_id=wallet.id,
            user_id=current_user.id,
            trans_id=refund_trans_id,
            amount=selling_price,
            type="credit",
            status="success",
            reference=f"REFUND-{transaction.id}",
            service_type="refund",
            meta_data=f"Refund for failed Electricity transaction {transaction.id}",
            profit=0.0
        )
        await wallet_repo.create_transaction(refund_transaction)

        # Send Refund Email
        EmailService.send_refund_email(
            background_tasks,
            current_user.email,
            current_user.full_name,
            f"Electricity {request.provider} {request.amount}",
            selling_price,
            refund_transaction.reference
        )

        raise HTTPException(status_code=400, detail=f"Transaction failed: {str(e)}")

    return {"message": "Electricity purchase successful", "transaction_id": transaction.id}

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
    """
    vtu_service = VTUAutomator()
    try:
        # Run blocking Selenium code in a separate thread
        details = await run_in_threadpool(vtu_service.get_sltv_user_details, request)
        if not details:
             raise HTTPException(status_code=404, detail="Could not retrieve details. Please check smart card number.")
        return {"status": "success", "data": details}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/tv")
async def purchase_tv(
    request: TVRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user),
    wallet_repo: WalletRepository = Depends(deps.get_wallet_repository),
):
    """
    Purchase TV subscription (e.g. SLTV).
    """
    wallet = await wallet_repo.get_by_user_id(current_user.id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")

    if wallet.balance < request.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

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
        meta_data=f"Provider: {request.provider}"
    )
    await wallet_repo.create_transaction(transaction)

    # Execute purchase synchronously
    vtu_service = VTUAutomator()
    from app.services.email_service import EmailService
    try:
        # Run blocking Selenium code in a separate thread
        result_message = await run_in_threadpool(vtu_service.purchase_tv, request)

        if result_message:
            # Success
            transaction.status = "success"
            transaction.meta_data += f" | Result: {result_message}"
            await wallet_repo.update_transaction(transaction)

            # Send Success Email
            EmailService.send_purchase_success_email(
                background_tasks,
                current_user.email,
                current_user.full_name,
                f"TV {request.provider} {request.amount}",
                request.amount,
                transaction.reference,
                request.smart_card_number
            )

            return {"status": "success", "message": result_message, "transaction_id": transaction.id}
        else:
            # Failed
            transaction.status = "failed"
            transaction.meta_data += " | Result: Failed to capture success message or error occurred."
            await wallet_repo.update_transaction(transaction)

            # Send Failed Email
            EmailService.send_purchase_failed_email(
                background_tasks,
                current_user.email,
                current_user.full_name,
                f"TV {request.provider} {request.amount}",
                request.amount,
                transaction.reference,
                "Failed to capture success message"
            )

            # Refund the user
            wallet.balance += request.amount
            await wallet_repo.update(wallet, {"balance": wallet.balance})

            # Create refund transaction
            refund_trans_id = generate_trans_id("REFUND")
            refund_transaction = Transaction(
                wallet_id=wallet.id,
                user_id=current_user.id,
                trans_id=refund_trans_id,
                amount=request.amount,
                type="credit",
                status="success",
                reference=f"REFUND-{transaction.id}",
                service_type="refund",
                meta_data=f"Refund for failed TV transaction {transaction.id}"
            )
            await wallet_repo.create_transaction(refund_transaction)

            # Send Refund Email
            EmailService.send_refund_email(
                background_tasks,
                current_user.email,
                current_user.full_name,
                f"TV {request.provider} {request.amount}",
                request.amount,
                refund_transaction.reference
            )

            raise HTTPException(status_code=400, detail="Transaction failed. Your wallet has been refunded.")

    except Exception as e:
        # Exception occurred
        transaction.status = "failed"
        transaction.meta_data += f" | Error: {str(e)}"
        await wallet_repo.update_transaction(transaction)

        # Send Failed Email
        EmailService.send_purchase_failed_email(
            background_tasks,
            current_user.email,
            current_user.full_name,
            f"TV {request.provider} {request.amount}",
            request.amount,
            transaction.reference,
            str(e)
        )

        # Refund the user
        wallet.balance += request.amount
        await wallet_repo.update(wallet, {"balance": wallet.balance})

        refund_trans_id = generate_trans_id("REFUND")
        refund_transaction = Transaction(
            wallet_id=wallet.id,
            user_id=current_user.id,
            trans_id=refund_trans_id,
            amount=request.amount,
            type="credit",
            status="success",
            reference=f"REFUND-{transaction.id}",
            service_type="refund",
            meta_data=f"Refund for failed TV transaction {transaction.id}"
        )
        await wallet_repo.create_transaction(refund_transaction)

        # Send Refund Email
        EmailService.send_refund_email(
            background_tasks,
            current_user.email,
            current_user.full_name,
            f"TV {request.provider} {request.amount}",
            request.amount,
            refund_transaction.reference
        )

        raise HTTPException(status_code=500, detail=f"Transaction failed with error: {str(e)}. Your wallet has been refunded.")
