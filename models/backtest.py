from typing import Union, Optional, Literal
from beanie import Document, PydanticObjectId
from pydantic import BaseModel

from models.stock import StockData
from models.strategy import Strategy, SMACrossoverParams, RSIParams, BreakoutParams
from models.trade import Trade


class PositionSizing(BaseModel):
    type: Literal['fixed', 'percentage']
    value: float


class BacktestResult(BaseModel):
    portfolio_cash: float
    portfolio_value: float
    sharpe_ratio: Optional[float]
    max_drawdown: float
    trade_list: list[Trade]


class BacktestBase(Document):
    class Settings:
        name = "backtests"

    id: Optional[PydanticObjectId] = None
    strategy: Strategy
    ticker: str
    start_time: int
    end_time: int
    initial_capital: float
    position_sizing: PositionSizing
    risk_free_rate: Optional[float] = 0
    strategy_params: Union[SMACrossoverParams, RSIParams, BreakoutParams]
    result: Optional[BacktestResult] = None


class Backtest(BacktestBase):
    id: PydanticObjectId


class BacktestResponse(BaseModel):
    stock_data: StockData
    result: BacktestResult
