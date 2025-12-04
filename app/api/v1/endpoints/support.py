from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from app.api import deps
from app.models.user import User
from app.models.support import Ticket, TicketMessage
from app.schemas.support import TicketCreate, TicketRead, TicketMessageCreate, TicketMessageRead
from app.repositories.support_repository import SupportRepository
from app.services.email_service import EmailService
import uuid

router = APIRouter()

@router.post("/", response_model=TicketRead)
async def create_ticket(
    *,
    ticket_in: TicketCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user),
    support_repo: SupportRepository = Depends(deps.get_support_repository),
) -> Any:
    """
    Create a new support ticket.
    """
    ticket = Ticket(
        user_id=current_user.id,
        subject=ticket_in.subject,
        priority=ticket_in.priority,
        status="open"
    )
    ticket = await support_repo.create_ticket(ticket)

    # Create initial message
    message = TicketMessage(
        ticket_id=ticket.id,
        sender_id=current_user.id,
        message=ticket_in.message,
        is_admin=False
    )
    await support_repo.create_message(message)

    # Send Email
    EmailService.send_ticket_created_email(
        background_tasks,
        current_user.email,
        current_user.full_name,
        str(ticket.id),
        ticket.subject,
        ticket_in.message
    )

    # Return ticket with message (need to fetch or construct)
    # For simplicity, let's fetch it fully
    return await support_repo.get_ticket_with_messages(ticket.id)

@router.get("/", response_model=List[TicketRead])
async def read_my_tickets(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_active_user),
    support_repo: SupportRepository = Depends(deps.get_support_repository),
) -> Any:
    """
    Retrieve current user's tickets.
    """
    return await support_repo.get_user_tickets(current_user.id, skip, limit)

@router.get("/{ticket_id}", response_model=TicketRead)
async def read_ticket(
    ticket_id: uuid.UUID,
    current_user: User = Depends(deps.get_current_active_user),
    support_repo: SupportRepository = Depends(deps.get_support_repository),
) -> Any:
    """
    Get ticket details and messages.
    """
    ticket = await support_repo.get_ticket_with_messages(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if ticket.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized to view this ticket")
    return ticket

@router.post("/{ticket_id}/message", response_model=TicketMessageRead)
async def reply_ticket(
    ticket_id: uuid.UUID,
    message_in: TicketMessageCreate,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(deps.get_current_active_user),
    support_repo: SupportRepository = Depends(deps.get_support_repository),
) -> Any:
    """
    Reply to a ticket.
    """
    ticket = await support_repo.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")
    if ticket.user_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(status_code=403, detail="Not authorized to reply to this ticket")

    is_admin = current_user.is_superuser

    message = TicketMessage(
        ticket_id=ticket.id,
        sender_id=current_user.id,
        message=message_in.message,
        is_admin=is_admin
    )
    await support_repo.create_message(message)

    # Update ticket updated_at
    from datetime import datetime
    await support_repo.update_ticket(ticket, {"updated_at": datetime.utcnow()})

    # Send Email Notification (if reply is from admin to user, or user to admin?)
    # Usually notify user if admin replies.
    # If user replies, maybe notify admin (optional, but good).
    # For now, let's implement Admin -> User notification here if current user is admin.
    # But wait, this endpoint is shared.

    if is_admin:
        # Admin replying to user
        # Need user email. Ticket has user_id.
        # Need to fetch user.
        # Let's assume we can get user from ticket.user if loaded, or fetch it.
        # support_repo.get_ticket might not load user.
        # Let's fetch user repo to get email.
        from app.repositories.user_repository import UserRepository
        # We can't easily inject another repo here without circular deps or complex setup?
        # Actually we can just use the session.
        user = await support_repo.session.get(User, ticket.user_id)
        if user:
             EmailService.send_ticket_reply_email(
                background_tasks,
                user.email,
                user.full_name,
                str(ticket.id),
                ticket.subject,
                message_in.message,
                is_admin_reply=True
            )

    return message
