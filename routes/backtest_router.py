from fastapi import APIRouter
from typing import Optional

from models.backtest import Backtest, BacktestBase, BacktestResponse
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
            response_model=Optional[BacktestResponse],
        )

    @staticmethod
    async def get_backtests() -> list[Backtest]:
        return await BacktestService.get_backtests()

    @staticmethod
    async def execute_backtest(backtest: BacktestBase) -> Optional[BacktestResponse]:
        result = await BacktestService.run_backtest(backtest)
        if result:
            stock_data, backtest_result = result
            return BacktestResponse(stock_data=stock_data, result=backtest_result)

        return result
