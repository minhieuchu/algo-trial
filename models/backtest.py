from typing import Union, Optional
from beanie import Document, PydanticObjectId

from models.strategy import Strategy, SimpleMovingAverageCrossover, RelativeStrengthIndex


class BacktestBase(Document):
    class Settings:
        name = "backtests"

    id: Optional[PydanticObjectId] = None
    strategy: Strategy
    logic: Union[SimpleMovingAverageCrossover, RelativeStrengthIndex]


class BacktestCreate(BacktestBase):
    pass


class Backtest(BacktestBase):
    id: PydanticObjectId
