from vnpy.app.cta_strategy import (
    CtaTemplate,
    StopOrder,
    TickData,
    BarData,
    TradeData,
    OrderData
)

from time import time


class SpotFuturesStrategy(CtaTemplate):
    """
    现货期货价差套利
    """
    author = "用Python的交易员"
    # 10个tick才触发
    test_trigger = 10

    tick_count = 0
    test_all_done = False
    # 参数列表，保存参数的名称
    parameters = ["test_trigger"]
    # 变量列表，保存了变量的名称
    variables = ["tick_count", "test_all_done"]

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        """"""
        super(SpotFuturesStrategy, self).__init__(
            cta_engine, strategy_name, vt_symbol, setting
        )
        # 需要测试的回调函数列表
        self.test_funcs = [
            self.test_market_order,
            self.test_limit_order,
            self.test_stop_order,
            self.test_cancel_all
        ]
        self.last_tick = None
        # True开启交易, False关闭交易
        self.trading = False

    def on_init(self):
        """
        Callback when strategy is inited.
        """
        self.write_log("策略初始化")

    def on_start(self):
        """
        Callback when strategy is started.
        """
        self.write_log("策略启动")

    def on_stop(self):
        """
        Callback when strategy is stopped.
        """
        self.write_log("策略停止")

    def on_tick(self, tick: TickData):
        """
        Callback of new tick data update.
        新的tick数据到来，更新一次
        """
        self.write_log(tick)

    def on_bar(self, bar: BarData):
        """
        Callback of new bar data update.
        """
        pass

    def on_order(self, order: OrderData):
        """
        Callback of new order data update.
        """
        self.put_event()

    def on_trade(self, trade: TradeData):
        """
        Callback of new trade data update.
        """
        self.put_event()

    def on_stop_order(self, stop_order: StopOrder):
        """
        Callback of stop order update.
        """
        self.put_event()

    def test_market_order(self):
        """"""
        r = self.buy(self.last_tick.bid_price_1, 1)
        print(r)
        self.write_log("执行市价单测试")

    def test_limit_order(self):
        """"""
        self.buy(self.last_tick.bid_price_1, 1)
        self.write_log("执行限价单测试")

    def test_stop_order(self):
        """"""
        self.buy(self.last_tick.ask_price_1, 1, True)
        self.write_log("执行停止单测试")

    def test_cancel_all(self):
        """"""
        self.cancel_all()
        self.write_log("执行全部撤单测试")
