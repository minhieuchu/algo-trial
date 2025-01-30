import backtrader as bt

from models.trade import Trade


class SmaCrossover(bt.Strategy):
    params = dict(
        pfast=10,  # default period for fast moving average
        pslow=30,  # default period for slow moving average
        ps_fixed=0.0,       # position sizing fixed
        ps_percentage=0.0,  # position sizing percentage
    )

    def __init__(self):
        sma1 = bt.ind.SMA(period=self.p.pfast)
        sma2 = bt.ind.SMA(period=self.p.pslow)
        self.crossover = bt.ind.CrossOver(sma1, sma2)
        self.trades: list[Trade] = []

    def next(self):
        if not self.position:
            if self.crossover > 0:
                cash = self.broker.get_cash()
                investment_amount = self.params.ps_fixed # noqa
                if self.params.ps_percentage > 0: # noqa
                    investment_amount = cash * self.params.ps_percentage # noqa

                share_price = self.data.close[0]
                share_size =  investment_amount // share_price

                self.buy(size=int(share_size))
        elif self.crossover < 0:
            self.close()

    def notify_trade(self, trade):
        bt_open_date = bt.num2date(trade.dtopen).timestamp()
        bt_close_date = bt.num2date(trade.dtclose).timestamp() if trade.dtclose > 0 else 0

        trade_model = Trade(
            size=trade.size,
            price=trade.price,
            value=trade.value,
            commission=trade.commission,
            pnl=trade.pnl,
            pnlcomm=trade.pnlcomm,
            isopen=trade.isopen,
            isclosed=trade.isclosed,
            dtopen=int(bt_open_date),
            dtclose=int(bt_close_date),
            status=trade.status,
            long=trade.long,
        )

        self.trades.append(trade_model)
