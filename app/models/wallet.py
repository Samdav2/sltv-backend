import uuid
from typing import Optional
from sqlmodel import SQLModel, Field

class WalletBase(SQLModel):
    balance: float = Field(default=0.0)
    currency: str = Field(default="NGN")

class Wallet(WalletBase, table=True):
    __tablename__ = "wallet"
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id", unique=True)
