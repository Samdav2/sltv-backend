from datetime import timedelta, datetime
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from app.core import security
from app.core.config import settings
from app.repositories.admin_repository import AdminRepository
from app.api import deps
from app.schemas.admin import AdminRead, AdminCreate, AdminUpdate, Token
from app.models.admin import Admin, AdminRole

router = APIRouter()

@router.post("/login/access-token", response_model=Token)
async def login_admin(
    form_data: OAuth2PasswordRequestForm = Depends(),
    admin_repo: AdminRepository = Depends(deps.get_admin_repository)
) -> Any:
    """
    Admin login.
    """
    admin = await admin_repo.get_by_email(form_data.username)
    if not admin or not security.verify_password(form_data.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    elif not admin.is_active:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive admin")

    # Update last_login
    admin.last_login = datetime.utcnow()
    await admin_repo.update(admin, {"last_login": admin.last_login})

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            admin.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.post("/create", response_model=AdminRead)
async def create_admin(
    *,
    admin_in: AdminCreate,
    admin_repo: AdminRepository = Depends(deps.get_admin_repository),
    # current_admin: Admin = Depends(deps.get_current_active_admin) # Uncomment to restrict to existing admins
) -> Any:
    """
    Create new admin.
    """
    admin = await admin_repo.get_by_email(admin_in.email)
    if admin:
        raise HTTPException(
            status_code=400,
            detail="The admin with this email already exists.",
        )

    admin_create = Admin(
        name=admin_in.name,
        email=admin_in.email,
        hashed_password=security.get_password_hash(admin_in.password),
        role=admin_in.role,
        is_active=True,
    )
    admin = await admin_repo.create(admin_create)
    return admin

@router.post("/change-password")
async def change_password(
    current_password: str,
    new_password: str,
    current_admin: Admin = Depends(deps.get_current_active_admin),
    admin_repo: AdminRepository = Depends(deps.get_admin_repository),
) -> Any:
    """
    Change current admin password.
    """
    if not security.verify_password(current_password, current_admin.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect password")

    hashed_password = security.get_password_hash(new_password)
    current_admin.hashed_password = hashed_password
    await admin_repo.update(current_admin, {"hashed_password": hashed_password})
    return {"message": "Password updated successfully"}

@router.post("/verify-email")
async def verify_email(
    token: str,
    admin_repo: AdminRepository = Depends(deps.get_admin_repository)
) -> Any:
    """
    Verify admin email (placeholder logic as Admin model doesn't have is_verified yet, but requested).
    """
    # Assuming we want to verify email, we might need to add is_verified to Admin model first.
    # For now, I'll just validate the token and return success if valid.
    email = security.verify_email_token(token, "verification")
    if not email:
        raise HTTPException(status_code=400, detail="Invalid token")

    admin = await admin_repo.get_by_email(email)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")

    if admin.is_verified:
        return {"message": "Email already verified"}

    admin.is_verified = True
    await admin_repo.update(admin, {"is_verified": True})

    return {"message": "Email verified successfully"}
