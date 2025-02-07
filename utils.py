from contextlib import asynccontextmanager
from beanie import init_beanie
from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient

from config import MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE
from models.backtest import Backtest


@asynccontextmanager
async def app_lifespan(_app: FastAPI):
    motor_client = AsyncIOMotorClient(f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DATABASE}")
    await init_beanie(motor_client.get_default_database(), document_models=[Backtest])
    yield
    motor_client.close()
