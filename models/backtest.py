from typing import Union, Optional
from beanie import Document, PydanticObjectId

from models.strategy import Strategy, SimpleMovingAverageCrossover, RelativeStrengthIndex


class BacktestBase(Document):
    class Settings:
        name = "backtests"

    id: Optional[PydanticObjectId] = None
    strategy: Strategy
    ticker: str
    start_time: int
    end_time: int
    initial_capital: float
    logic: Union[SimpleMovingAverageCrossover, RelativeStrengthIndex]


class Backtest(BacktestBase):
    id: PydanticObjectId
