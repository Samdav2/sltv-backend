from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from app.core.config import settings

# Handle Database URL for Async Drivers
database_url = settings.DATABASE_URL

if database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql+asyncpg://", 1)
elif database_url.startswith("postgresql://"):
    database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
elif database_url.startswith("sqlite"):
    database_url = database_url.replace("sqlite://", "sqlite+aiosqlite://")

# Engine Configuration
engine_args = {
    "echo": False,  # Set to False for production performance
    "future": True,
}

# Add connection pooling for PostgreSQL
if "postgresql" in database_url:
    engine_args.update({
        "pool_size": 20,
        "max_overflow": 10,
        "pool_pre_ping": True,  # Handles disconnected connections
    })

engine = create_async_engine(database_url, **engine_args)

async def get_session() -> AsyncSession:
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
