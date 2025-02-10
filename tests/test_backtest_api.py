from models.backtest import BacktestBase, PositionSizing
from models.strategy import Strategy, SMACrossoverParams
from tests.conftest import RUN_BACKTEST_URL, LIST_BACKTESTS_URL


def test_run_backtest_succeed(test_db, test_client):
    backtest_base = BacktestBase(
        strategy=Strategy.SMACrossover,
        ticker="AAPL",
        start_time=1650042000,
        end_time=1725123600,
        initial_capital=100000,
        position_sizing=PositionSizing(fixed=0, percentage=0.1),
        logic=SMACrossoverParams(fast_sma_period=10, slow_sma_period=30),
    )
    test_client.post(RUN_BACKTEST_URL, json=backtest_base.model_dump(mode="json"))
    backtest_response = test_client.get(LIST_BACKTESTS_URL)
    backtest_list = backtest_response.json()

    assert len(backtest_list) ==  1

def test_run_backtest_fail_time(test_db, test_client):
    # Start time is equal to end time
    backtest_base_1 = BacktestBase(
        strategy=Strategy.SMACrossover,
        ticker="AAPL",
        start_time=1650042000,
        end_time=1650042000,
        initial_capital=100000,
        risk_free_rate=0.0,
        position_sizing=PositionSizing(fixed=0, percentage=0.1),
        logic=SMACrossoverParams(fast_sma_period=10, slow_sma_period=30),
    )
    # Start time is larger than end time
    backtest_base_2 = BacktestBase(
        strategy=Strategy.SMACrossover,
        ticker="AAPL",
        start_time=1650042000,
        end_time=1600042000,
        initial_capital=100000,
        risk_free_rate=0.0,
        position_sizing=PositionSizing(fixed=0, percentage=0.1),
        logic=SMACrossoverParams(fast_sma_period=10, slow_sma_period=30),
    )

    test_client.post(RUN_BACKTEST_URL, json=backtest_base_1.model_dump(mode="json"))
    test_client.post(RUN_BACKTEST_URL, json=backtest_base_2.model_dump(mode="json"))

    backtest_response = test_client.get(LIST_BACKTESTS_URL)
    backtest_list = backtest_response.json()

    assert len(backtest_list) == 0

def test_run_backtest_fail_ticker(test_db, test_client):
    # Missing ticker
    backtest_base_1 = BacktestBase(
        strategy=Strategy.SMACrossover,
        ticker="",
        start_time=1650042000,
        end_time=1725123600,
        initial_capital=100000,
        risk_free_rate=0.0,
        position_sizing=PositionSizing(fixed=0, percentage=0.1),
        logic=SMACrossoverParams(fast_sma_period=10, slow_sma_period=30),
    )
    # Non-existent ticker
    backtest_base_2 = BacktestBase(
        strategy=Strategy.SMACrossover,
        ticker="___",
        start_time=1650042000,
        end_time=1725123600,
        initial_capital=100000,
        risk_free_rate=0.0,
        position_sizing=PositionSizing(fixed=0, percentage=0.1),
        logic=SMACrossoverParams(fast_sma_period=10, slow_sma_period=30),
    )

    test_client.post(RUN_BACKTEST_URL, json=backtest_base_1.model_dump(mode="json"))
    test_client.post(RUN_BACKTEST_URL, json=backtest_base_2.model_dump(mode="json"))

    backtest_response = test_client.get(LIST_BACKTESTS_URL)
    backtest_list = backtest_response.json()

    assert len(backtest_list) == 1
