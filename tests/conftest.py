import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from sqlmodel.pool import StaticPool

from app.main import app
from app.core.database import get_session
from app.services.automation_service import VTUAutomator

@pytest.fixture(name="session")
async def session_fixture():
    engine = create_async_engine(
        "sqlite+aiosqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )
    async with async_session() as session:
        yield session

@pytest.fixture(name="client")
async def client_fixture(session: AsyncSession):
    async def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture(autouse=True)
def mock_automator(monkeypatch):
    # Create a mock class or instance
    class MockVTUAutomator:
        def purchase_airtime(self, request):
            return True
        def purchase_data(self, request):
            return True
        def purchase_electricity(self, request):
            return True
        def purchase_tv(self, request):
            return "Success"
        def get_sltv_user_details(self, request):
            return {"name": "Test User"}

    # Patch the class itself to return our mock instance (or behave like one)
    # Since VTUAutomator is a singleton using __new__, patching the class might be tricky if we want to replace the whole thing.
    # But services.py does `vtu_automator = VTUAutomator()`.
    # If we replace the class name in the module, it should work.

    monkeypatch.setattr("app.api.v1.endpoints.services.VTUAutomator", MockVTUAutomator)
