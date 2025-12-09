import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

# --- Message Schemas ---
class TicketMessageBase(BaseModel):
    message: str

class TicketMessageCreate(TicketMessageBase):
    pass

class TicketMessageRead(TicketMessageBase):
    id: uuid.UUID
    ticket_id: uuid.UUID
    sender_id: Optional[uuid.UUID] = None
    admin_id: Optional[uuid.UUID] = None
    created_at: datetime
    is_admin: bool

    class Config:
        orm_mode = True

# --- Ticket Schemas ---
class TicketBase(BaseModel):
    subject: str
    priority: str = "medium"

class TicketCreate(TicketBase):
    message: str # Initial message

class TicketUpdate(BaseModel):
    status: Optional[str] = None
    priority: Optional[str] = None

class TicketRead(TicketBase):
    id: uuid.UUID
    user_id: uuid.UUID
    status: str
    created_at: datetime
    updated_at: datetime
    messages: List[TicketMessageRead] = []

    class Config:
        orm_mode = True
