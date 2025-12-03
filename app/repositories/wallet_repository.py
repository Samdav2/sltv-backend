import uuid
from typing import List, Optional
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from app.repositories.base import BaseRepository
from app.models.wallet import Wallet
from app.models.transaction import Transaction

class WalletRepository(BaseRepository[Wallet]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Wallet)

    async def get_by_user_id(self, user_id: uuid.UUID) -> Optional[Wallet]:
        statement = select(Wallet).where(Wallet.user_id == user_id)
        result = await self.session.exec(statement)
        return result.first()

    async def create_transaction(self, transaction: Transaction) -> Transaction:
        self.session.add(transaction)
        await self.session.commit()
        await self.session.refresh(transaction)
        return transaction

    async def get_transactions(self, wallet_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[Transaction]:
        statement = select(Transaction).where(Transaction.wallet_id == wallet_id).offset(skip).limit(limit)
        result = await self.session.exec(statement)
        return result.all()

    async def update_transaction(self, transaction: Transaction) -> Transaction:
        self.session.add(transaction)
        await self.session.commit()
        await self.session.refresh(transaction)
        return transaction
