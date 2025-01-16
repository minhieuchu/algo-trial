from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from fastapi import FastAPI

from models.backtest import Backtest


async def app_lifespan(_app: FastAPI):
    motor_client = AsyncIOMotorClient("mongodb://localhost:27017/algo_trial")
    await init_beanie(motor_client.get_default_database(), document_models=[Backtest])
    yield
    motor_client.close()
