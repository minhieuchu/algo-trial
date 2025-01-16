from typing import Optional

from models.backtest import Backtest, BacktestCreate


class BacktestRepository:
    async def get_backtests(self) -> list[Backtest]:
        return await Backtest.find_all().to_list()

    async def create_backtest(self, backtest_create: BacktestCreate) -> tuple[bool, Optional[Backtest]]:
        status = False
        result: Optional[Backtest] = None
        try:
            result: Backtest = await backtest_create.insert()
            status = True
        except Exception as e:
            print("Mongodb insert error: ", e)

        return status, result
