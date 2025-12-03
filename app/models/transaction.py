import uuid
from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field, Relationship

class TransactionBase(SQLModel):
    amount: float
    type: str  # "credit" or "debit"
    status: str = "pending"
    reference: str
    service_type: Optional[str] = None
    meta_data: Optional[str] = None
    profit: float = Field(default=0.0)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Transaction(TransactionBase, table=True):
    __tablename__ = "transaction"
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    trans_id: Optional[str] = Field(default=None, index=True) # External ID (e.g. for MobileNig)
    wallet_id: uuid.UUID = Field(foreign_key="wallet.id")
    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="transactions")
