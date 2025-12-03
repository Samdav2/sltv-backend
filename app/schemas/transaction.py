import uuid
from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class TransactionBase(BaseModel):
    amount: float
    type: str
    status: str = "pending"
    reference: str
    service_type: Optional[str] = None
    meta_data: Optional[str] = None
    created_at: datetime

class TransactionRead(TransactionBase):
    id: uuid.UUID
    wallet_id: uuid.UUID

class TransactionCreate(TransactionBase):
    wallet_id: uuid.UUID
