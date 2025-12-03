from typing import Generic, TypeVar, Type, List, Optional, Any
from sqlmodel import select, SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from app.models.user import User

ModelType = TypeVar("ModelType", bound=SQLModel)

class BaseRepository(Generic[ModelType]):
    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    async def get(self, id: Any) -> Optional[ModelType]:
        stmt = select(User).where(User.id == id)
        payload = await self.session.exec(stmt)
        result = payload.first()
        return result

    async def get_all(self, skip: int = 0, limit: int = 100) -> List[ModelType]:
        statement = select(self.model).offset(skip).limit(limit)
        result = await self.session.exec(statement)
        return result.all()

    async def create(self, obj_in: ModelType) -> ModelType:
        self.session.add(obj_in)
        await self.session.commit()
        await self.session.refresh(obj_in)
        return obj_in

    async def update(self, db_obj: ModelType, obj_in: dict | ModelType) -> ModelType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_obj, key, value)

        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, id: Any) -> Optional[ModelType]:
        obj = await self.session.get(self.model, id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
        return obj
