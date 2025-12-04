import uuid
from typing import List, Optional
from sqlmodel import select, desc
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.support import Ticket, TicketMessage

class SupportRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_ticket(self, ticket: Ticket) -> Ticket:
        self.session.add(ticket)
        await self.session.commit()
        await self.session.refresh(ticket)
        return ticket

    async def create_message(self, message: TicketMessage) -> TicketMessage:
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def get_ticket(self, ticket_id: uuid.UUID) -> Optional[Ticket]:
        # Eager load messages? SQLModel doesn't support joinedload easily in async yet without SQLAlchemy imports
        # But accessing .messages might trigger lazy load if session is active, or we fetch manually.
        # For simple use case, let's fetch ticket.
        # To ensure messages are loaded, we might need select options or separate query if lazy loading fails in async.
        # Let's try standard get first.
        ticket = await self.session.get(Ticket, ticket_id)
        return ticket

    async def get_ticket_with_messages(self, ticket_id: uuid.UUID) -> Optional[Ticket]:
        from sqlalchemy.orm import selectinload
        statement = select(Ticket).where(Ticket.id == ticket_id).options(selectinload(Ticket.messages))
        result = await self.session.exec(statement)
        return result.first()

    async def get_user_tickets(self, user_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Ticket]:
        from sqlalchemy.orm import selectinload
        statement = select(Ticket).where(Ticket.user_id == user_id).options(selectinload(Ticket.messages)).order_by(desc(Ticket.updated_at)).offset(skip).limit(limit)
        result = await self.session.exec(statement)
        return result.all()

    async def get_all_tickets(self, skip: int = 0, limit: int = 100) -> List[Ticket]:
        from sqlalchemy.orm import selectinload
        statement = select(Ticket).options(selectinload(Ticket.messages)).order_by(desc(Ticket.updated_at)).offset(skip).limit(limit)
        result = await self.session.exec(statement)
        return result.all()

    async def update_ticket(self, ticket: Ticket, update_data: dict) -> Ticket:
        for key, value in update_data.items():
            setattr(ticket, key, value)
        self.session.add(ticket)
        await self.session.commit()
        await self.session.refresh(ticket)
        return ticket
