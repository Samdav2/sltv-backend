from typing import Optional, List
import uuid
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.admin import Admin
from app.repositories.base import BaseRepository

class AdminRepository(BaseRepository[Admin]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Admin)

    async def get_by_email(self, email: str) -> Optional[Admin]:
        statement = select(Admin).where(Admin.email == email)
        result = await self.session.exec(statement)
        return result.first()
