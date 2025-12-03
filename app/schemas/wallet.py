import uuid
from typing import Optional
from pydantic import BaseModel

class WalletBase(BaseModel):
    balance: float = 0.0
    currency: str = "NGN"

class WalletRead(WalletBase):
    id: uuid.UUID
    user_id: uuid.UUID

class WalletUpdate(BaseModel):
    balance: Optional[float] = None
