import os
from urllib.parse import urlparse
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from app.core.config import settings


def _resolve_database_url() -> str:
    database_url = settings.DATABASE_URL or "sqlite+aiosqlite:///./app.db"

    if database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql+asyncpg://", 1)
    elif database_url.startswith("postgresql://"):
        database_url = database_url.replace("postgresql://", "postgresql+asyncpg://", 1)
    elif database_url.startswith("sqlite://"):
        database_url = database_url.replace("sqlite://", "sqlite+aiosqlite://", 1)

    is_railway_or_cloud = bool(
        os.getenv("RAILWAY_ENVIRONMENT")
        or os.getenv("RAILWAY_SERVICE_NAME")
        or os.getenv("PORT")
        or os.path.exists("/.dockerenv")
    )

    if "postgresql" in database_url and not is_railway_or_cloud:
        hostname = urlparse(database_url).hostname
        if hostname in {"db", "postgres", "postgresql"}:
            return "sqlite+aiosqlite:///./app.db"

    return database_url


# Handle Database URL for Async Drivers
database_url = _resolve_database_url()

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
