from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from app.api import deps
from app.models.user import User
from app.models.user_profile import UserProfile
from app.schemas.user_profile import UserProfileCreate, UserProfileRead, UserProfileUpdate
from app.repositories.profile_repository import ProfileRepository

router = APIRouter()

@router.get("/me", response_model=UserProfileRead)
async def get_my_profile(
    current_user: User = Depends(deps.get_current_active_user),
    profile_repo: ProfileRepository = Depends(deps.get_profile_repository),
) -> Any:
    """
    Get current user's profile.
    """
    profile = await profile_repo.get_by_user_id(current_user.id)

    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile

@router.post("/me", response_model=UserProfileRead)
async def create_or_update_profile(
    profile_in: UserProfileUpdate,
    current_user: User = Depends(deps.get_current_active_user),
    profile_repo: ProfileRepository = Depends(deps.get_profile_repository),
) -> Any:
    """
    Create or update current user's profile.
    """
    profile = await profile_repo.get_by_user_id(current_user.id)

    if profile:
        # Update
        return await profile_repo.update(profile, profile_in)
    else:
        # Create
        # We need to convert UserProfileUpdate to UserProfile, but UserProfile needs user_id
        # UserProfileUpdate doesn't have user_id.
        # So we create a dict and add user_id.
        profile_data = profile_in.model_dump()
        profile_data["user_id"] = current_user.id
        new_profile = UserProfile(**profile_data)
        return await profile_repo.create(new_profile)
