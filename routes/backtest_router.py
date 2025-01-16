from fastapi import APIRouter

from services.backtest_service import BacktestService
from models.backtest import BacktestCreate


class BacktestRouter:
    def __init__(self):
        self.route = APIRouter(prefix="/backtests")
        self.route.add_api_route(path="", endpoint=self.get_backtests, methods=["GET"])
        self.route.add_api_route(path="", endpoint=self.create_backtest, methods=["POST"])

    @staticmethod
    async def get_backtests():
        return await BacktestService.get_backtests()

    @staticmethod
    async def create_backtest(backtest: BacktestCreate):
        result = await BacktestService.create_backtest(backtest)
        return result
