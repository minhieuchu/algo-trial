import backtrader as bt
from datetime import datetime
import pandas as pd
import yfinance as yf

from models.backtest import Backtest, BacktestBase
from models.strategy import Strategy
from repositories.backtest_repository import BacktestRepository
from strategies.SmaCrossover import SmaCrossover


class BacktestService:
    @staticmethod
    async def get_backtests():
        result = await BacktestRepository().get_backtests()
        return result

    @staticmethod
    async def execute_backtest(backtest: BacktestBase) -> Backtest:
        start_time = datetime.fromtimestamp(backtest.start_time).strftime("%Y-%m-%d")
        end_time = datetime.fromtimestamp(backtest.end_time).strftime("%Y-%m-%d")

        df = yf.download(backtest.ticker, start=start_time, end=end_time)
        df.columns = [col[0] for col in df.columns]
        df.index = pd.to_datetime(df.index)
        data = bt.feeds.PandasData(dataname=df)

        cerebro = bt.Cerebro()
        cerebro.broker.setcash(backtest.initial_capital)
        cerebro.adddata(data)

        if backtest.strategy == Strategy.SMA:
            cerebro.addstrategy(
                SmaCrossover,
                pfast=backtest.logic.fast_sma_period,
                pslow=backtest.logic.slow_sma_period,
            )
            cerebro.run()

        _, created_backtest = await BacktestRepository().save_backtest(
            backtest
        )
        return created_backtest
