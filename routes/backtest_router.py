from fastapi import APIRouter

from models.backtest import Backtest, BacktestBase, BacktestResult
from services.backtest_service import BacktestService


class BacktestRouter:
    def __init__(self):
        self.route = APIRouter(prefix="/backtests")
        self.route.add_api_route(
            path="",
            endpoint=self.get_backtests,
            methods=["GET"],
            response_model=list[Backtest],
        )
        self.route.add_api_route(
            path="",
            endpoint=self.execute_backtest,
            methods=["POST"],
            response_model=BacktestResult,
        )

    @staticmethod
    async def get_backtests() -> list[Backtest]:
        return await BacktestService.get_backtests()

    @staticmethod
    async def execute_backtest(backtest: BacktestBase) -> BacktestResult:
        result = await BacktestService.execute_backtest(backtest)
        return result
