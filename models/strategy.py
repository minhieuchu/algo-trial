from enum import StrEnum
from pydantic import BaseModel


class Strategy(StrEnum):
    SMA = "SMA"
    RSI = "RSI"


class SMACrossoverParams(BaseModel):
    fast_sma_period: int
    slow_sma_period: int


class RSIParams(BaseModel):
    rsi_period: int
    rsi_low: float
    rsi_high: float
