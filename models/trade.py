from pydantic import BaseModel


class Trade(BaseModel):
    size: int
    price: float
    value: float
    commission: float
    pnl: float
    pnlcomm: float
    isopen: bool
    isclosed: bool
    dtopen: int
    dtclose: int
    status: int
    long: bool
