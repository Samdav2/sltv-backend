from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Request
from typing import Any
from app.services.mobilenig_service import mobilenig_service
from app.schemas.mobilenig import (
    BalanceResponse,
    ServicesStatusResponse,
    CustomerValidationRequest,
    CustomerValidationResponse,
    AirtimePurchaseRequest,
    DataPurchaseRequest,
    ElectricityPurchaseRequest,
    CablePurchaseRequest,
    PurchaseResponse,
    QueryTransactionResponse,
)
from app.models.user import User
from app.models.transaction import Transaction
from app.models.service_price import ServicePrice, ProfitType
from app.repositories.wallet_repository import WalletRepository
from app.api import deps
from app.core.limiter import limiter
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

@router.get("/balance", response_model=BalanceResponse)
async def get_balance(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get MobileNig wallet balance.
    """
    try:
        return await mobilenig_service.get_balance()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/services", response_model=ServicesStatusResponse)
async def get_services(
    service_id: str = "All",
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get status of MobileNig services.
    """
    try:
        return await mobilenig_service.get_services_status(service_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/validate", response_model=CustomerValidationResponse)
async def validate_customer(
    request: CustomerValidationRequest,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Validate customer details (SmartCard, Meter No, etc.).
    """
    try:
        return await mobilenig_service.validate_customer(request.service_id, request.customerAccountId)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/purchase/airtime", response_model=PurchaseResponse)
@limiter.limit("10/minute")
async def purchase_airtime(
    request: Request,
    purchase_req: AirtimePurchaseRequest,
    current_user: User = Depends(deps.get_current_active_user),
    wallet_repo: WalletRepository = Depends(deps.get_wallet_repository),
    session: deps.AsyncSession = Depends(deps.get_session),
) -> Any:
    """
    Purchase Airtime.
    """
    cost_price = purchase_req.amount
    profit = 0.0

    # 1. Calculate Price or use Admin Amount
    if purchase_req.admin_amount is not None:
        selling_price = purchase_req.admin_amount
        # If admin amount is set, profit is selling_price - cost_price
        profit = selling_price - cost_price
    else:
        service_identifier = f"airtime-{purchase_req.service_id.lower()}"
        statement = select(ServicePrice).where(ServicePrice.service_identifier == service_identifier)
        result = await session.exec(statement)
        price_config = result.first()

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

    trans_id = generate_trans_id("AIRTIME")

    transaction = Transaction(
        wallet_id=wallet.id,
        user_id=current_user.id,
        trans_id=trans_id,
        amount=selling_price,
        type="debit",
        status="processing",
        reference=f"AIRTIME-{wallet.id}-{purchase_req.phoneNumber}",
        service_type="airtime",
        meta_data=f"Network: {purchase_req.service_id}",
        profit=profit
    )
    await wallet_repo.create_transaction(transaction)

    try:
        payload = purchase_req.model_dump()
        payload["trans_id"] = trans_id
        # User Data Injection
        payload["email"] = current_user.email
        payload["customerName"] = current_user.full_name or ""
        payload["address"] = current_user.profile.address if current_user.profile else ""

        response = await mobilenig_service.purchase_service(payload)

        transaction.status = "success"
        transaction.meta_data += f" | Response: {response}"
        await wallet_repo.update_transaction(transaction)
        return response
    except Exception as e:
        transaction.status = "failed"
        transaction.meta_data += f" | Error: {str(e)}"
        await wallet_repo.update_transaction(transaction)

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
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/purchase/data", response_model=PurchaseResponse)
@limiter.limit("10/minute")
async def purchase_data(
    request: Request,
    purchase_req: DataPurchaseRequest,
    current_user: User = Depends(deps.get_current_active_user),
    wallet_repo: WalletRepository = Depends(deps.get_wallet_repository),
    session: deps.AsyncSession = Depends(deps.get_session),
) -> Any:
    """
    Purchase Data Bundle.
    """
    cost_price = purchase_req.amount
    profit = 0.0

    # 1. Calculate Price or use Admin Amount
    if purchase_req.admin_amount is not None:
        selling_price = purchase_req.admin_amount
        profit = selling_price - cost_price
    else:
        service_identifier = f"data-{purchase_req.service_id.lower()}"
        statement = select(ServicePrice).where(ServicePrice.service_identifier == service_identifier)
        result = await session.exec(statement)
        price_config = result.first()

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
        reference=f"DATA-{wallet.id}-{purchase_req.phoneNumber}",
        service_type="data",
        meta_data=f"Network: {purchase_req.service_id}, Plan: {purchase_req.productCode}",
        profit=profit
    )
    await wallet_repo.create_transaction(transaction)

    try:
        # Construct payload manually to ensure correct mapping
        payload = {
            "service_id": purchase_req.productCode,
            "phoneNumber": purchase_req.phoneNumber,
            "amount": cost_price,
            "trans_id": trans_id,
            "email": current_user.email,
            "customerName": current_user.full_name or ""
        }
        # Add address if available
        if current_user.profile and current_user.profile.address:
             payload["address"] = current_user.profile.address

        response = await mobilenig_service.purchase_service(payload)

        transaction.status = "success"
        transaction.meta_data += f" | Response: {response}"
        await wallet_repo.update_transaction(transaction)
        return response
    except Exception as e:
        transaction.status = "failed"
        transaction.meta_data += f" | Error: {str(e)}"
        await wallet_repo.update_transaction(transaction)

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
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/purchase/electricity", response_model=PurchaseResponse)
@limiter.limit("10/minute")
async def purchase_electricity(
    request: Request,
    purchase_req: ElectricityPurchaseRequest,
    current_user: User = Depends(deps.get_current_active_user),
    wallet_repo: WalletRepository = Depends(deps.get_wallet_repository),
    session: deps.AsyncSession = Depends(deps.get_session),
) -> Any:
    """
    Pay Electricity Bill.
    """
    cost_price = purchase_req.amount
    profit = 0.0

    # 1. Calculate Price or use Admin Amount
    if purchase_req.admin_amount is not None:
        selling_price = purchase_req.admin_amount
        profit = selling_price - cost_price
    else:
        service_identifier = f"electricity-{purchase_req.service_id.lower()}"
        statement = select(ServicePrice).where(ServicePrice.service_identifier == service_identifier)
        result = await session.exec(statement)
        price_config = result.first()

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

    transaction = Transaction(
        wallet_id=wallet.id,
        user_id=current_user.id,
        trans_id=trans_id,
        amount=selling_price,
        type="debit",
        status="processing",
        reference=f"ELEC-{wallet.id}-{purchase_req.meterNumber}",
        service_type="electricity",
        meta_data=f"Provider: {purchase_req.service_id}",
        profit=profit
    )
    await wallet_repo.create_transaction(transaction)

    try:
        payload = purchase_req.model_dump()
        payload["trans_id"] = trans_id
        # User Data Injection
        if not payload.get("email"):
            payload["email"] = current_user.email

        response = await mobilenig_service.purchase_service(payload)

        transaction.status = "success"
        transaction.meta_data += f" | Response: {response}"
        await wallet_repo.update_transaction(transaction)
        return response
    except Exception as e:
        transaction.status = "failed"
        transaction.meta_data += f" | Error: {str(e)}"
        await wallet_repo.update_transaction(transaction)

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
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/purchase/cable", response_model=PurchaseResponse)
@limiter.limit("10/minute")
async def purchase_cable(
    request: Request,
    purchase_req: CablePurchaseRequest,
    current_user: User = Depends(deps.get_current_active_user),
    wallet_repo: WalletRepository = Depends(deps.get_wallet_repository),
    session: deps.AsyncSession = Depends(deps.get_session),
) -> Any:
    """
    Subscribe to Cable TV (DSTV, GOTV, Startimes).
    """
    cost_price = purchase_req.amount
    profit = 0.0

    # 1. Calculate Price or use Admin Amount
    if purchase_req.admin_amount is not None:
        selling_price = purchase_req.admin_amount
        profit = selling_price - cost_price
    else:
        service_identifier = f"cable-{purchase_req.service_id.lower()}"
        statement = select(ServicePrice).where(ServicePrice.service_identifier == service_identifier)
        result = await session.exec(statement)
        price_config = result.first()

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

    trans_id = generate_trans_id("CABLE")

    transaction = Transaction(
        wallet_id=wallet.id,
        user_id=current_user.id,
        trans_id=trans_id,
        amount=selling_price,
        type="debit",
        status="processing",
        reference=f"CABLE-{wallet.id}-{purchase_req.smartcardNumber}",
        service_type="cable",
        meta_data=f"Provider: {purchase_req.service_id}",
        profit=profit
    )
    await wallet_repo.create_transaction(transaction)

    try:
        payload = purchase_req.model_dump(exclude_none=True)
        payload["trans_id"] = trans_id
        # User Data Injection
        payload["email"] = current_user.email
        if not payload.get("customerName"):
             payload["customerName"] = current_user.full_name or ""
        payload["address"] = current_user.profile.address if current_user.profile else ""

        response = await mobilenig_service.purchase_service(payload)

        transaction.status = "success"
        transaction.meta_data += f" | Response: {response}"
        await wallet_repo.update_transaction(transaction)
        return response
    except Exception as e:
        transaction.status = "failed"
        transaction.meta_data += f" | Error: {str(e)}"
        await wallet_repo.update_transaction(transaction)

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
            meta_data=f"Refund for failed Cable transaction {transaction.id}",
            profit=0.0
        )
        await wallet_repo.create_transaction(refund_transaction)
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/query/{trans_id}", response_model=QueryTransactionResponse)
async def query_transaction(
    trans_id: str,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Query a transaction status.
    """
    try:
        return await mobilenig_service.query_transaction(trans_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
