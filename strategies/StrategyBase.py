from abc import abstractmethod, ABCMeta
import backtrader as bt
from typing import Dict

from models.trade import Trade
from strategies.constants import default_strategy_params


class StrategyMeta(type(bt.Strategy), ABCMeta):
    pass


class StrategyBase(bt.Strategy, metaclass=StrategyMeta):
    params = default_strategy_params

    def __init__(self):
        self.trades: list[Trade] = []
        self.trade_sizes: Dict[int, float] = {}

    @abstractmethod
    def next(self):
        pass

    def notify_trade(self, trade):
        bt_open_date = bt.num2date(trade.dtopen).timestamp()
        bt_close_date = bt.num2date(trade.dtclose).timestamp() if trade.dtclose > 0 else 0

        trade_price = trade.price
        if trade.isopen:
            self.trade_sizes[trade.ref] = trade.size
        else:
            trade_size = self.trade_sizes[trade.ref]
            if trade.long:
                trade_price = trade.price + (trade.pnl / trade_size)
            else:
                trade_price = trade.price - (trade.pnl / trade_size)

        trade_model = Trade(
            ref=trade.ref,
            size=trade.size,
            price=trade_price,
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

    def _get_buy_size(self) -> int:
        cash = self.broker.get_cash()
        investment_amount = self.params.ps_value  # noqa
        if self.params.ps_type == "percentage":  # noqa
            investment_amount = cash * self.params.ps_value / 100  # noqa

        share_price = self.data.close[0]
        share_size = investment_amount // share_price

        return int(share_size)
