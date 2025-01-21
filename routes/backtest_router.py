from fastapi import APIRouter

from models.backtest import BacktestBase
from services.backtest_service import BacktestService


class BacktestRouter:
    def __init__(self):
        self.route = APIRouter(prefix="/backtests")
        self.route.add_api_route(path="", endpoint=self.get_backtests, methods=["GET"])
        self.route.add_api_route(path="", endpoint=self.execute_backtest, methods=["POST"])

    @staticmethod
    async def get_backtests():
        return await BacktestService.get_backtests()

    @staticmethod
    async def execute_backtest(backtest: BacktestBase):
        result = await BacktestService.execute_backtest(backtest)
        return result
