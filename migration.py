import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie

from config import MONGODB_HOST, MONGODB_PORT, MONGODB_DATABASE
from models.backtest import Backtest, BacktestResult, BacktestBase
from services.backtest_service import BacktestService


async def migration_script():
    motor_client = AsyncIOMotorClient(
        f"mongodb://{MONGODB_HOST}:{MONGODB_PORT}"
    )
    database = motor_client[MONGODB_DATABASE]
    await init_beanie(database, document_models=[Backtest])

    # Put migration logic here
    # await Backtest.find({"strategy": "SMA"}).update(
    #     {"$set": {"strategy": Strategy.SMACrossover}}
    # )
    # await Backtest.find({"position_sizing": {"$exists": False}}).update_many(
    #     {"$set": {"position_sizing": {"fixed": 0, "percentage": 0.05}}}
    # )

    backtest_collection = database["backtests"]
    backtest_documents = await backtest_collection.find().to_list()

    for backtest in backtest_documents:
        try:
            BacktestResult.model_validate(backtest.get('result'))
        except Exception as e:
            print("Validation Error: ", e)
            backtest.pop("result")
            backtest_base = BacktestBase.model_validate(backtest)
            backtest_result = await BacktestService.run_backtest(backtest_base)

            await Backtest.find_one({"_id": backtest_base.id}).update({"$set": {"result": backtest_result}})


if __name__ == "__main__":
    asyncio.run(migration_script())
