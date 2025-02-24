import pytest

from models.backtest import BacktestBase, PositionSizing
from models.strategy import Strategy, SMACrossoverParams
from services.backtest_service import BacktestService


@pytest.mark.asyncio
async def test_run_backtest_succeed(test_db):
    backtest_base = BacktestBase(
        strategy=Strategy.SMACrossover,
        ticker="AAPL",
        start_time=1650042000,
        end_time=1725123600,
        initial_capital=100000,
        risk_free_rate=0.0,
        position_sizing=PositionSizing(type="percentage", value=0.1),
        strategy_params=SMACrossoverParams(fast_sma_period=10, slow_sma_period=30),
    )
    await BacktestService.run_backtest(backtest_base)
    backtest_list = await BacktestService.get_backtests()
    assert len(backtest_list) == 1

@pytest.mark.asyncio
async def test_run_backtest_fail_time(test_db):
   # Start time is equal to end time
   backtest_base_1 = BacktestBase(
      strategy=Strategy.SMACrossover,
      ticker="AAPL",
      start_time=1650042000,
      end_time=1650042000,
      initial_capital=100000,
      risk_free_rate=0.0,
      position_sizing=PositionSizing(type="percentage", value=0.1),
      strategy_params=SMACrossoverParams(fast_sma_period=10, slow_sma_period=30),
   )
   # Start time is larger than end time
   backtest_base_2 = BacktestBase(
       strategy=Strategy.SMACrossover,
       ticker="AAPL",
       start_time=1650042000,
       end_time=1600042000,
       initial_capital=100000,
       risk_free_rate=0.0,
       position_sizing=PositionSizing(type="percentage", value=0.1),
       strategy_params=SMACrossoverParams(fast_sma_period=10, slow_sma_period=30),
   )
   await BacktestService.run_backtest(backtest_base_1)
   await BacktestService.run_backtest(backtest_base_2)

   backtest_list = await BacktestService.get_backtests()
   assert len(backtest_list) == 0


@pytest.mark.asyncio
async def test_run_backtest_fail_ticker(test_db):
    # Missing ticker
    backtest_base_1 = BacktestBase(
        strategy=Strategy.SMACrossover,
        ticker="",
        start_time=1650042000,
        end_time=1725123600,
        initial_capital=100000,
        risk_free_rate=0.0,
        position_sizing=PositionSizing(type="percentage", value=0.1),
        strategy_params=SMACrossoverParams(fast_sma_period=10, slow_sma_period=30),
    )
    # Non-existent ticker
    backtest_base_2 = BacktestBase(
        strategy=Strategy.SMACrossover,
        ticker="___",
        start_time=1650042000,
        end_time=1725123600,
        initial_capital=100000,
        risk_free_rate=0.0,
        position_sizing=PositionSizing(type="percentage", value=0.1),
        strategy_params=SMACrossoverParams(fast_sma_period=10, slow_sma_period=30),
    )
    await BacktestService.run_backtest(backtest_base_1)
    await BacktestService.run_backtest(backtest_base_2)

    backtest_list = await BacktestService.get_backtests()
    assert len(backtest_list) == 0
