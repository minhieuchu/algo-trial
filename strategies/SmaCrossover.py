import backtrader as bt


class SmaCrossover(bt.Strategy):
    params = dict(
        pfast=10,  # default period for fast moving average
        pslow=30,  # default period for slow moving average
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)
        sma2 = bt.ind.SMA(period=self.p.pslow)
        self.crossover = bt.ind.CrossOver(sma1, sma2)

    def next(self):
        if not self.position:  # not in the market
            if self.crossover > 0:  # fast crosses slow to the upside
                self.buy()  # enter long
        elif self.crossover < 0:  # in the market & cross to the downside
            self.close()  # close long position

    def notify_trade(self, trade):
        if trade.isclosed:
            print(f"Trade Closed: PnL Gross={trade.pnl:.2f}, Net={trade.pnlcomm:.2f}")
        elif trade.isopen:
            print(f"Trade Opened: Size={trade.size}, Price={trade.price:.2f}")
