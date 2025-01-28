import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from config import MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE
from models.backtest import Backtest


async def migration_script():
    motor_client = AsyncIOMotorClient(f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DATABASE}")
    await init_beanie(motor_client.get_default_database(), document_models=[Backtest])

    # Put migration logic here

if __name__ == "__main__":
    asyncio.run(migration_script())
