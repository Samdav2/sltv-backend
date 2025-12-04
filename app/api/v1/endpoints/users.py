from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from app.repositories.user_repository import UserRepository
from app.api import deps
from app.models.user import User
from app.schemas.user import UserCreate, UserRead
from app.core import security

router = APIRouter()

@router.post("/", response_model=UserRead)
async def create_user(
    *,
    user_in: UserCreate,
    background_tasks: BackgroundTasks,
    user_repo: UserRepository = Depends(deps.get_user_repository),
    wallet_repo: deps.WalletRepository = Depends(deps.get_wallet_repository),
) -> Any:
    """
    Create new user.
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
        is_superuser=False,
    )
    user = await user_repo.create(user_create)

    # Create wallet for the user
    from app.models.wallet import Wallet
    wallet = Wallet(user_id=user.id, balance=0.0, currency="NGN")
    await wallet_repo.create(wallet)

    # Send Welcome Email
    from app.services.email_service import EmailService
    EmailService.send_user_welcome_email(background_tasks, user.email, user.full_name)

    # Send Verification Email
    from app.core.config import settings

    # Generate verification token
    verification_token = security.create_email_token(user.email, "verification")

    # Use a default URL if FRONTEND_URL is not set (or add it to config)
    frontend_url = getattr(settings, "FRONTEND_URL", "http://localhost:3000")
    verification_link = f"{frontend_url}/verify-email?token={verification_token}"

    EmailService.send_email_verification(background_tasks, user.email, user.full_name, verification_link)

    return user
