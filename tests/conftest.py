import pytest
import pytest_asyncio
from httpx import AsyncClient, ASGITransport

from app.main import app
from app.services import shipment_service


@pytest.fixture(autouse=True)
def clear_store() -> None:
    """Wipe the in-memory store before every test for isolation."""
    shipment_service.clear_all()


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac
