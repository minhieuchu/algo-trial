import pytest_asyncio
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE_TEST
from models.backtest import Backtest


@pytest_asyncio.fixture(scope="function")
async def test_db():
    motor_client = AsyncIOMotorClient(
        f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}"
    )
    database = motor_client[MONGODB_DATABASE_TEST]
    await init_beanie(database, document_models=[Backtest])
    yield
    await motor_client.drop_database(MONGODB_DATABASE_TEST)
    motor_client.close()
