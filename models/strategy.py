from enum import StrEnum
from pydantic import BaseModel


class Strategy(StrEnum):
    SMA = "SMA"
    RST = "RSI"


class SimpleMovingAverageCrossover(BaseModel):
    short_term_length: int
    long_term_length: int


class RelativeStrengthIndex(BaseModel):
    buy_rsi: int
    sell_rsi: int
