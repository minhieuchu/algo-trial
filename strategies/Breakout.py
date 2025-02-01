import backtrader as bt

from strategies.StrategyBase import StrategyBase
from strategies.constants import default_strategy_params


class Breakout(StrategyBase):
    _params = dict(lookback=20)
    params = {**default_strategy_params, **_params}

    def __init__(self):
        super().__init__()
        self.highest = bt.ind.Highest(self.data.high, period=self.p.lookback)  # noqa
        self.lowest = bt.ind.Lowest(self.data.low, period=self.p.lookback)  # noqa

    def next(self):
        if not self.position:
            if self.data.close[0] > self.highest[-1]:
                size = self._get_buy_size()
                self.buy(size=size)
        elif self.data.close[0] < self.lowest[-1]:
            self.close()
