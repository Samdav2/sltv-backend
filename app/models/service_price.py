import uuid
from typing import Optional
from sqlmodel import SQLModel, Field
from enum import Enum

class ProfitType(str, Enum):
    FIXED = "fixed"
    PERCENTAGE = "percentage"

class ServicePriceBase(SQLModel):
    service_identifier: str = Field(index=True, unique=True) # e.g. "airtime-mtn", "electricity-aedc"
    profit_type: ProfitType = ProfitType.FIXED
    profit_value: float = 0.0

class ServicePrice(ServicePriceBase, table=True):
    __tablename__ = "service_price"
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
