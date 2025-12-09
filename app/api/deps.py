import uuid
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlmodel.ext.asyncio.session import AsyncSession
from app.core import security
from app.core.config import settings
from app.core.database import get_session
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app.repositories.wallet_repository import WalletRepository
from app.repositories.profile_repository import ProfileRepository
from app.models.admin import Admin
from app.repositories.admin_repository import AdminRepository

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login/access-token"
)

async def get_user_repository(session: AsyncSession = Depends(get_session)) -> UserRepository:
    return UserRepository(session)

async def get_wallet_repository(session: AsyncSession = Depends(get_session)) -> WalletRepository:
    return WalletRepository(session)

async def get_profile_repository(session: AsyncSession = Depends(get_session)) -> ProfileRepository:
    return ProfileRepository(session)

async def get_admin_repository(session: AsyncSession = Depends(get_session)) -> AdminRepository:
    return AdminRepository(session)

async def get_current_user(
    token: str = Depends(reusable_oauth2),
    user_repo: UserRepository = Depends(get_user_repository),
) -> User:
    try:
        payload = jwt.decode(
            token, settings.JWT_PUBLIC_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = payload.get("sub")
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = await user_repo.get(uuid.UUID(str(token_data)))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_active_superuser(
    current_user: User = Depends(get_current_active_user),
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user

from app.repositories.support_repository import SupportRepository
async def get_support_repository(session: AsyncSession = Depends(get_session)) -> SupportRepository:
    return SupportRepository(session)

async def get_current_admin(
    token: str = Depends(reusable_oauth2),
    admin_repo: AdminRepository = Depends(get_admin_repository),
) -> Admin:
    try:
        payload = jwt.decode(
            token, settings.JWT_PUBLIC_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = payload.get("sub")
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    # Try to convert token_data to UUID
    try:
        admin_id = uuid.UUID(str(token_data))
    except ValueError:
         raise HTTPException(status_code=403, detail="Invalid token format")

    admin = await admin_repo.get(admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin

async def get_current_active_admin(
    current_admin: Admin = Depends(get_current_admin),
) -> Admin:
    if not current_admin.is_active:
        raise HTTPException(status_code=400, detail="Inactive admin")
    return current_admin
