import backtrader as bt

from strategies.StrategyBase import StrategyBase
from strategies.constants import default_strategy_params


class RSI(StrategyBase):
    _params = dict(
        rsi_period=14,
        rsi_low=30,
        rsi_high=70
    )
    params = {**default_strategy_params, **_params}

    def __init__(self):
        super().__init__()
        self.rsi = bt.indicators.RSI(period=self.params.rsi_period) # noqa

    def next(self):
        if not self.position:
            if self.rsi < self.params.rsi_low:  # noqa
                self.buy(size=self._get_buy_size())
        else:
            if self.rsi > self.params.rsi_high: # noqa
                self.sell()
