from fastapi import APIRouter, Depends, HTTPException
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


router = APIRouter()

@router.get("/balance", response_model=BalanceResponse)
def get_balance() -> Any:
    """
    Get MobileNig wallet balance.
    """
    try:
        return mobilenig_service.get_balance()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/services", response_model=ServicesStatusResponse)
def get_services(service_id: str = "All") -> Any:
    """
    Get status of MobileNig services.
    """
    try:
        return mobilenig_service.get_services_status(service_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/validate", response_model=CustomerValidationResponse)
def validate_customer(request: CustomerValidationRequest) -> Any:
    """
    Validate customer details (SmartCard, Meter No, etc.).
    """
    try:
        return mobilenig_service.validate_customer(request.service_id, request.customerAccountId)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/purchase/airtime", response_model=PurchaseResponse)
def purchase_airtime(request: AirtimePurchaseRequest) -> Any:
    """
    Purchase Airtime.
    """
    try:
        payload = request.model_dump()
        return mobilenig_service.purchase_service(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/purchase/data", response_model=PurchaseResponse)
def purchase_data(request: DataPurchaseRequest) -> Any:
    """
    Purchase Data Bundle.
    """
    try:
        payload = request.model_dump(by_alias=True)
        return mobilenig_service.purchase_service(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/purchase/electricity", response_model=PurchaseResponse)
def purchase_electricity(request: ElectricityPurchaseRequest) -> Any:
    """
    Pay Electricity Bill.
    """
    try:
        payload = request.model_dump()
        return mobilenig_service.purchase_service(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.post("/purchase/cable", response_model=PurchaseResponse)
def purchase_cable(request: CablePurchaseRequest) -> Any:
    """
    Subscribe to Cable TV (DSTV, GOTV, Startimes).
    """
    try:
        payload = request.model_dump(exclude_none=True)
        return mobilenig_service.purchase_service(payload)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/query/{trans_id}", response_model=QueryTransactionResponse)
def query_transaction(trans_id: str) -> Any:
    """
    Query a transaction status.
    """
    try:
        return mobilenig_service.query_transaction(trans_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
