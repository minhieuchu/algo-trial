from fastapi import APIRouter
from typing import Optional

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
            response_model=Optional[BacktestResult],
        )

    @staticmethod
    async def get_backtests() -> list[Backtest]:
        return await BacktestService.get_backtests()

    @staticmethod
    async def execute_backtest(backtest: BacktestBase) -> Optional[BacktestResult]:
        result = await BacktestService.run_backtest(backtest)
        return result
