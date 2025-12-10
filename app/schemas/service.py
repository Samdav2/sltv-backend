from typing import Optional
from sqlmodel import SQLModel

class AirtimeRequest(SQLModel):
    phone_number: str
    amount: float
    network: str

class DataRequest(SQLModel):
    phone_number: str
    plan_id: str
    network: str
    amount: float

class ElectricityRequest(SQLModel):
    meter_number: str
    amount: float
    provider: str
    type: str = "prepaid"  # prepaid or postpaid

class ElectricityVerifyRequest(SQLModel):
    meter_number: str
    provider: str
    type: str = "prepaid"

class TVRequest(SQLModel):
    smart_card_number: str
    amount: float
    provider: str = "sltv" # Default to SLTV as requested

class TVRefreshRequest(SQLModel):
    smart_card_number: str
    provider: str = "sltv"
