from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from app.api import deps
from app.models.user import User
from app.models.admin import Admin
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.schemas.transaction import TransactionRead
from app.repositories.user_repository import UserRepository
from app.repositories.wallet_repository import WalletRepository
from app.core import security
import uuid

router = APIRouter()

# --- User Management ---

@router.get("/users", response_model=List[UserRead])
async def read_users(
    skip: int = 0,
    limit: int = 100,
    current_admin: Admin = Depends(deps.get_current_active_admin),
    user_repo: UserRepository = Depends(deps.get_user_repository),
) -> Any:
    """
    Retrieve users.
    """
    # Note: UserRepository might need a get_multi method.
    # If not present, we'll need to add it or use session directly.
    # Assuming get_multi exists or similar. If not, I'll use session.
    # Let's check user_repo in next step if this fails, but usually standard repo has it.
    # For now, I'll assume it might not and use the session from repo if accessible or just implement basic list.
    # Actually, let's implement a basic list using the session attached to repo.
    from sqlmodel import select
    statement = select(User).offset(skip).limit(limit)
    result = await user_repo.session.exec(statement)
    users = result.all()
    return users

@router.post("/users", response_model=UserRead)
async def create_user(
    *,
    user_in: UserCreate,
    current_admin: Admin = Depends(deps.get_current_active_admin),
    user_repo: UserRepository = Depends(deps.get_user_repository),
    wallet_repo: deps.WalletRepository = Depends(deps.get_wallet_repository),
) -> Any:
    """
    Create new user (by admin).
    """
    user = await user_repo.get_by_email(user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system.",
        )

    user_create = User(
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
        full_name=user_in.full_name,
        is_active=True,
        is_superuser=False, # Admin can create normal users. To create admin, update later.
    )
    user = await user_repo.create(user_create)

    # Create wallet
    from app.models.wallet import Wallet
    wallet = Wallet(user_id=user.id, balance=0.0, currency="NGN")
    await wallet_repo.create(wallet)

    return user

@router.get("/users/{user_id}", response_model=UserRead)
async def read_user_by_id(
    user_id: uuid.UUID,
    current_admin: Admin = Depends(deps.get_current_active_admin),
    user_repo: UserRepository = Depends(deps.get_user_repository),
) -> Any:
    """
    Get a specific user by id.
    """
    user = await user_repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/users/{user_id}", response_model=UserRead)
async def update_user(
    *,
    user_id: uuid.UUID,
    user_in: UserUpdate,
    current_admin: Admin = Depends(deps.get_current_active_admin),
    user_repo: UserRepository = Depends(deps.get_user_repository),
) -> Any:
    """
    Update a user.
    """
    user = await user_repo.get(user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="The user with this id does not exist in the system",
        )
    user = await user_repo.update(user, user_in.dict(exclude_unset=True))
    return user

@router.post("/users/{user_id}/reset-password")
async def reset_user_password(
    user_id: uuid.UUID,
    new_password: str, # In query or body? Better in body usually but simpler here.
    current_admin: Admin = Depends(deps.get_current_active_admin),
    user_repo: UserRepository = Depends(deps.get_user_repository),
) -> Any:
    """
    Reset a user's password manually.
    """
    user = await user_repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    hashed_password = security.get_password_hash(new_password)
    user.hashed_password = hashed_password
    await user_repo.update(user, {"hashed_password": hashed_password})
    return {"message": "Password updated successfully"}


# --- Transaction Management ---

@router.get("/transactions", response_model=List[TransactionRead])
async def read_transactions(
    skip: int = 0,
    limit: int = 100,
    current_admin: Admin = Depends(deps.get_current_active_admin),
    wallet_repo: WalletRepository = Depends(deps.get_wallet_repository),
) -> Any:
    """
    Retrieve all transactions (system-wide).
    """
    # Need to access transaction table directly or add method to repo.
    # Using session from repo for direct access.
    from app.models.transaction import Transaction
    from sqlmodel import select, desc

    statement = select(Transaction).order_by(desc(Transaction.created_at)).offset(skip).limit(limit)
    result = await wallet_repo.session.exec(statement)
    transactions = result.all()
    return transactions

@router.get("/transactions/{transaction_id}", response_model=TransactionRead)
async def read_transaction(
    transaction_id: uuid.UUID,
    current_admin: Admin = Depends(deps.get_current_active_admin),
    wallet_repo: WalletRepository = Depends(deps.get_wallet_repository),
) -> Any:
    """
    Get specific transaction.
    """
    from app.models.transaction import Transaction
    # If ID is int or UUID?
    # I'll try to fetch by ID.
    transaction = await wallet_repo.session.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

# --- Support Management ---

from app.schemas.support import TicketRead, TicketUpdate
from app.repositories.support_repository import SupportRepository

@router.get("/support/tickets", response_model=List[TicketRead])
async def read_all_tickets(
    skip: int = 0,
    limit: int = 100,
    current_admin: Admin = Depends(deps.get_current_active_admin),
    support_repo: SupportRepository = Depends(deps.get_support_repository),
) -> Any:
    """
    Retrieve all support tickets.
    """
    return await support_repo.get_all_tickets(skip, limit)

@router.put("/support/tickets/{ticket_id}/status", response_model=TicketRead)
async def update_ticket_status(
    ticket_id: uuid.UUID,
    status_update: TicketUpdate,
    current_admin: Admin = Depends(deps.get_current_active_admin),
    support_repo: SupportRepository = Depends(deps.get_support_repository),
) -> Any:
    """
    Update ticket status or priority.
    """
    ticket = await support_repo.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    update_data = status_update.dict(exclude_unset=True)
    ticket = await support_repo.update_ticket(ticket, update_data)
    return ticket

from app.schemas.support import TicketMessageCreate, TicketMessageRead
from app.models.support import TicketMessage
from fastapi import BackgroundTasks
from app.services.email_service import EmailService

@router.post("/support/tickets/{ticket_id}/message", response_model=TicketMessageRead)
async def reply_ticket(
    ticket_id: uuid.UUID,
    message_in: TicketMessageCreate,
    background_tasks: BackgroundTasks,
    current_admin: Admin = Depends(deps.get_current_active_admin),
    support_repo: SupportRepository = Depends(deps.get_support_repository),
) -> Any:
    """
    Reply to a ticket as admin.
    """
    ticket = await support_repo.get_ticket(ticket_id)
    if not ticket:
        raise HTTPException(status_code=404, detail="Ticket not found")

    message = TicketMessage(
        ticket_id=ticket.id,
        admin_id=current_admin.id,
        sender_id=None, # Admin reply
        message=message_in.message,
        is_admin=True
    )
    await support_repo.create_message(message)

    # Update ticket updated_at
    from datetime import datetime
    await support_repo.update_ticket(ticket, {"updated_at": datetime.utcnow()})

    # Send Email Notification to User
    # Fetch user to get email
    from app.models.user import User
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
