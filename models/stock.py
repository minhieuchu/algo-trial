from pydantic import BaseModel
from typing import Dict


class StockEnty(BaseModel):
    Open: float
    Close: float
    High: float
    Low: float
    Volume: int


StockData = Dict[str, StockEnty]
