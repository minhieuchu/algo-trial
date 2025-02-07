import asyncio
import pytest
from beanie import init_beanie
import pytest_asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.testclient import TestClient

from config import MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE_TEST
from http_service import HttpService
from models.backtest import Backtest


RUN_BACKTEST_URL = "/v1/backtests"
LIST_BACKTESTS_URL = "/v1/backtests"

@pytest_asyncio.fixture(scope="function")
async def test_db():
    motor_client = AsyncIOMotorClient(
        f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}"
    )
    motor_client.get_io_loop = asyncio.get_event_loop
    database = motor_client[MONGODB_DATABASE_TEST]
    await init_beanie(database, document_models=[Backtest])
    yield
    await motor_client.drop_database(MONGODB_DATABASE_TEST)
    motor_client.close()

@pytest.fixture(scope="session")
def test_client():
    test_client = TestClient(HttpService().get_app())
    return test_client
