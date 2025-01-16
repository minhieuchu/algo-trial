from models.backtest import Backtest, BacktestCreate
from repositories.backtest_repository import BacktestRepository


class BacktestService:
    @staticmethod
    async def get_backtests():
        result = await BacktestRepository().get_backtests()
        return result

    @staticmethod
    async def create_backtest(backtest_create: BacktestCreate):
        _, created_backtest = await BacktestRepository().create_backtest(backtest_create)
        return created_backtest
