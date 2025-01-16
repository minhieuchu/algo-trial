from fastapi import APIRouter

from services.backtest_service import BacktestService


class BacktestAPI:
    def __init__(self):
        self.route = APIRouter(prefix="/backtests")
        self.route.add_api_route(path="", endpoint=self.run_backtest, methods=["POST"])

    @staticmethod
    async def run_backtest():
        BacktestService.execute_backtest()
