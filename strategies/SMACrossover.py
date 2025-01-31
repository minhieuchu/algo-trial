import backtrader as bt

from strategies.StrategyBase import StrategyBase
from strategies.constants import default_strategy_params


class SMACrossover(StrategyBase):
    _params = dict(
        pfast=10,  # default period for fast moving average
        pslow=30,  # default period for slow moving average
    )
    params = {**default_strategy_params, **_params}

    def __init__(self):
        super().__init__()
        sma1 = bt.ind.SMA(period=self.p.pfast)  # noqa
        sma2 = bt.ind.SMA(period=self.p.pslow)  # noqa
        self.crossover = bt.ind.CrossOver(sma1, sma2)  # noqa

    def next(self):
        if not self.position:
            if self.crossover > 0:
                self.buy(size=self._get_buy_size())
        elif self.crossover < 0:
            self.close()
