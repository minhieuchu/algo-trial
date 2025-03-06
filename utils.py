import asyncio
from beanie import init_beanie
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.routing import APIRoute
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.routing import Match

from config import MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE
from models.backtest import Backtest


request_queue = asyncio.Queue()

async def process_queue(app: FastAPI):
    scope = await request_queue.get()
    for route in app.routes:
        match_result, _ = route.matches(scope)
        if match_result == Match.FULL and isinstance(route, APIRoute):
            if "body" in scope:
                request_body = scope["body"]
                data = await route.endpoint(request_body)
            else:
                data = await route.endpoint()

@asynccontextmanager
async def app_lifespan(app: FastAPI):
    # Init MongoDB client
    motor_client = AsyncIOMotorClient(f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}/{MONGODB_DATABASE}")
    await init_beanie(motor_client.get_default_database(), document_models=[Backtest])

    # Run background task that processes requests for rate limiter
    asyncio.create_task(process_queue(app))

    yield
    motor_client.close()
