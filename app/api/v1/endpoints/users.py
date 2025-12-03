from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
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

    return user
