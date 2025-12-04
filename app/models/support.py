import uuid
from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

class TicketBase(SQLModel):
    subject: str
    priority: str = "medium" # low, medium, high
    status: str = "open" # open, in_progress, closed, resolved
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class Ticket(TicketBase, table=True):
    __tablename__ = "ticket"
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")

    # Relationships
    user: Optional["User"] = Relationship(back_populates="tickets")
    messages: List["TicketMessage"] = Relationship(back_populates="ticket")

class TicketMessageBase(SQLModel):
    message: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    is_admin: bool = False # True if sent by admin/support

class TicketMessage(TicketMessageBase, table=True):
    __tablename__ = "ticket_message"
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    ticket_id: uuid.UUID = Field(foreign_key="ticket.id")
    sender_id: uuid.UUID = Field(foreign_key="user.id")

    # Relationships
    ticket: Optional[Ticket] = Relationship(back_populates="messages")
    sender: Optional["User"] = Relationship()
