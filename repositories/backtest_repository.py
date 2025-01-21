from typing import Optional

from models.backtest import Backtest, BacktestBase


class BacktestRepository:
    async def get_backtests(self) -> list[Backtest]:
        return await Backtest.find_all().to_list()

    async def save_backtest(self, backtest: BacktestBase) -> tuple[bool, Optional[Backtest]]:
        status = False
        result: Optional[Backtest] = None
        try:
            result: Backtest = await backtest.insert()
            status = True
        except Exception as e:
            print("Mongodb insert error: ", e)

        return status, result
