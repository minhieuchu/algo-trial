import backtrader as bt
from datetime import datetime
import pandas as pd
import yfinance as yf
from typing import Optional

from models.backtest import Backtest, BacktestBase, BacktestResult
from models.strategy import Strategy
from repositories.backtest_repository import BacktestRepository
from strategies.Breakout import Breakout
from strategies.SMACrossover import SMACrossover
from strategies.RSI import RSI


class BacktestService:
    @staticmethod
    async def get_backtests() -> list[Backtest]:
        result = await BacktestRepository().get_backtests()
        return result

    @staticmethod
    async def execute_backtest(backtest: BacktestBase) -> Optional[BacktestResult]:
        start_time = datetime.fromtimestamp(backtest.start_time).strftime("%Y-%m-%d")
        end_time = datetime.fromtimestamp(backtest.end_time).strftime("%Y-%m-%d")

        try:
            df = yf.download(backtest.ticker, start=start_time, end=end_time)
        except Exception as e:
            print("Download ticker data error: ", e)
            return None

        df.columns = [col[0] for col in df.columns]
        df.index = pd.to_datetime(df.index)
        data = bt.feeds.PandasData(dataname=df)  # noqa

        cerebro = bt.Cerebro()
        cerebro.broker.setcash(backtest.initial_capital)
        cerebro.adddata(data)
        cerebro.addanalyzer(
            bt.analyzers.SharpeRatio,
            _name="sharpe_ratio",
            riskfreerate=backtest.risk_free_rate,
        )
        cerebro.addanalyzer(bt.analyzers.DrawDown, _name="drawdown")

        if backtest.strategy == Strategy.SMACrossover:
            cerebro.addstrategy(
                SMACrossover,
                pfast=backtest.logic.fast_sma_period,
                pslow=backtest.logic.slow_sma_period,
                ps_fixed=backtest.position_sizing.fixed,
                ps_percentage=backtest.position_sizing.percentage,
            )

        if backtest.strategy == Strategy.RSI:
            cerebro.addstrategy(
                RSI,
                rsi_period=backtest.logic.rsi_period,
                rsi_low=backtest.logic.rsi_low,
                rsi_high=backtest.logic.rsi_high,
                ps_fixed=backtest.position_sizing.fixed,
                ps_percentage=backtest.position_sizing.percentage,
            )

        if backtest.strategy == Strategy.Breakout:
            cerebro.addstrategy(
                Breakout,
                lookback=backtest.logic.lookback,
                ps_fixed=backtest.position_sizing.fixed,
                ps_percentage=backtest.position_sizing.percentage,
            )

        try:
            results = cerebro.run()
        except Exception as e:
            print("Backtrader Cerebro Exception: ", e)
            return None

        sharpe_ratio = results[0].analyzers.sharpe_ratio.get_analysis()
        drawdown_analysis = results[0].analyzers.drawdown.get_analysis()

        backtest_result = BacktestResult(
            portfolio_cash=cerebro.broker.get_cash(),
            portfolio_value=cerebro.broker.get_value(),
            sharpe_ratio=sharpe_ratio["sharperatio"],
            max_drawdown=drawdown_analysis["max"]["drawdown"],
            trade_list=results[0].trades,
        )
        backtest.result = backtest_result

        await BacktestRepository().save_backtest(backtest)

        return backtest_result
