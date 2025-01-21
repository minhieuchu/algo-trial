from enum import StrEnum
from pydantic import BaseModel


class Strategy(StrEnum):
    SMA = "SMA"
    RST = "RSI"


class SimpleMovingAverageCrossover(BaseModel):
    fast_sma_period: int
    slow_sma_period: int


class RelativeStrengthIndex(BaseModel):
    buy_rsi: int
    sell_rsi: int
