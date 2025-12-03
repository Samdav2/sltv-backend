from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from app.models.user import User
from app.models.user_profile import UserProfile
from app.schemas.user_profile import UserProfileCreate, UserProfileRead, UserProfileUpdate
from sqlmodel import select

router = APIRouter()

@router.get("/me", response_model=UserProfileRead)
async def get_my_profile(
    current_user: User = Depends(deps.get_current_active_user),
    session: deps.AsyncSession = Depends(deps.get_session),
) -> Any:
    """
    Get current user's profile.
    """
    # Check if profile exists
    # Since we added the relationship, we might be able to access it directly if eager loaded,
    # but safe to query.
    statement = select(UserProfile).where(UserProfile.user_id == current_user.id)
    result = await session.exec(statement)
    profile = result.first()

    if not profile:
        # Return empty profile or 404?
        # Usually better to return empty or create one if it doesn't exist.
        # Let's return 404 for now as per standard REST, or empty fields if the schema allows.
        # But the user asked for "request for gettin gcurrent user for all edpoinf in the services".
        # Let's return 404 if not set.
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.post("/me", response_model=UserProfileRead)
async def create_or_update_profile(
    profile_in: UserProfileUpdate,
    current_user: User = Depends(deps.get_current_active_user),
    session: deps.AsyncSession = Depends(deps.get_session),
) -> Any:
    """
    Create or update current user's profile.
    """
    statement = select(UserProfile).where(UserProfile.user_id == current_user.id)
    result = await session.exec(statement)
    profile = result.first()

    if profile:
        # Update
        profile_data = profile_in.dict(exclude_unset=True)
        for key, value in profile_data.items():
            setattr(profile, key, value)
        session.add(profile)
        await session.commit()
        await session.refresh(profile)
        return profile
    else:
        # Create
        profile = UserProfile(**profile_in.dict(), user_id=current_user.id)
        session.add(profile)
        await session.commit()
        await session.refresh(profile)
        return profile
