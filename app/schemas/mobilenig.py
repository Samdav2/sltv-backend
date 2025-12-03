from typing import Optional, List, Any, Union
from pydantic import BaseModel, Field, AliasChoices

class MobileNigBaseResponse(BaseModel):
    message: str
    statusCode: str
    details: Any

class BalanceDetails(BaseModel):
    balance: Union[str, float, int]

class BalanceResponse(MobileNigBaseResponse):
    details: BalanceDetails

class ServiceStatus(BaseModel):
    service: str
    name: str
    status: str
    blocked: bool

class ServicesStatusResponse(MobileNigBaseResponse):
    details: Union[List[ServiceStatus], ServiceStatus, str, Any]

class CustomerValidationRequest(BaseModel):
    service_id: str
    customerAccountId: str

class CustomerValidationDetails(BaseModel):
    firstName: Optional[str] = None
    lastName: Optional[str] = None
    customerName: Optional[str] = Field(None, validation_alias="name")
    address: Optional[str] = None
    dueDate: Optional[str] = None
    amount: Optional[float] = None
    customerNumber: Optional[str] = Field(None, validation_alias=AliasChoices("meterNumber", "smartCardNumber", "customerNumber"))
    accountStatus: Optional[str] = None
    invoicePeriod: Optional[int] = None
    customerType: Optional[str] = Field(None, validation_alias="customerAccountType")

class CustomerValidationResponse(MobileNigBaseResponse):
    details: Union[CustomerValidationDetails, str, Any]

class AirtimePurchaseRequest(BaseModel):
    service_id: str
    amount: float
    phoneNumber: str

class DataPurchaseRequest(BaseModel):
    service_id: str
    service_type: Optional[str] = None
    amount: float
    phoneNumber: str = Field(validation_alias="customerPhoneNumber", serialization_alias="beneficiary")
    productCode: str = Field(validation_alias="productCode", serialization_alias="code")

    class Config:
        populate_by_name = True

class ElectricityPurchaseRequest(BaseModel):
    service_id: str
    amount: float
    meterNumber: str
    phoneNumber: str
    email: str
    customerName: str
    customerAddress: str
    customerAccountType: str
    customerDtNumber: str
    contactType: str

class CablePurchaseRequest(BaseModel):
    service_id: str
    amount: float
    smartcardNumber: str
    customerNumber: Optional[str] = None
    customerName: Optional[str] = None
    productCode: Optional[str] = None # Required if changing subscription

class PurchaseDetails(BaseModel):
    trans_id: str
    service: str
    status: str
    details: dict
    wallet_balance: Union[str, float, int]

class PurchaseResponse(MobileNigBaseResponse):
    details: Union[PurchaseDetails, str, Any]

class QueryTransactionResponse(MobileNigBaseResponse):
    details: Union[PurchaseDetails, str, Any]
