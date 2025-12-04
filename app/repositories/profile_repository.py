from typing import Optional
import uuid
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.repositories.base import BaseRepository
from app.models.user_profile import UserProfile

class ProfileRepository(BaseRepository[UserProfile]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, UserProfile)

    async def get_by_user_id(self, user_id: uuid.UUID) -> Optional[UserProfile]:
        statement = select(UserProfile).where(UserProfile.user_id == user_id)
        result = await self.session.exec(statement)
        return result.first()
