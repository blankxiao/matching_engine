"""
Author:  Blank
Date: 2024/6/27
Description: 
"""
from collections import deque
from .Order import  Order
from .Trade import Trade
from .TradingDao import TradingDao
class OrderBook:
    def __init__(self, db: TradingDao):
        self.db = db
        self.buy_orders = deque()
        self.sell_orders = deque()
        self.trades = []

        self.load_orders()
        self.load_trades()

    def load_orders(self):
        # 获取所有未完成的订单
        orders = self.db.get_all_orders(status="uncompleted")
        for order in orders:

            if order.order_type == "buy":
                self.buy_orders.append(order)
            elif order.order_type == "sell":
                self.sell_orders.append(order)

        # 按价格排序买单和卖单
        self.buy_orders = deque(sorted(self.buy_orders, key=lambda x: x.price, reverse=True))
        self.sell_orders = deque(sorted(self.sell_orders, key=lambda x: x.price))


    def load_trades(self):
        # 获取所有交易
        trades = self.db.get_all_trades()
        for trade in trades:
            self.trades.append(trade)


    def add_order(self, order):
        new_order = self.db.insert_order(order)
        self.display_new_order(new_order)
        # 根据类型进行排序
        if order.order_type == "buy":
            self.buy_orders.append(new_order)
            self.buy_orders = deque(sorted(self.buy_orders, key=lambda x: x.price, reverse=True))
        elif order.order_type == "sell":
            self.sell_orders.append(new_order)
            self.sell_orders = deque(sorted(self.sell_orders, key=lambda x: x.price))


    def match_orders(self):
        while self.buy_orders and self.sell_orders:
            buy_order = self.buy_orders[0]
            sell_order = self.sell_orders[0]

            if buy_order.price >= sell_order.price:
                trade_quantity = min(buy_order.quantity, sell_order.quantity)
                trade_price = sell_order.price

                buy_order.quantity -= trade_quantity
                sell_order.quantity -= trade_quantity
                new_trade = Trade(buy_order, sell_order, trade_price, trade_quantity)
                self.trades.append(new_trade)

                self.db.update_order(buy_order)
                self.db.update_order(sell_order)
                new_trade = self.db.insert_trade(new_trade)
                self.trades.append(new_trade)
                self.display_new_trade(new_trade)

                if buy_order.quantity == 0:
                    self.buy_orders.popleft()
                if sell_order.quantity == 0:
                    self.sell_orders.popleft()
            else:
                break

    def display_order_book(self):
        print("买入需求:")
        flag = True
        for order in self.buy_orders:
            flag = False
            print(order)
        if flag:
            print("暂无买入")
        print()

        flag = True
        print("卖出需求:")
        for order in self.sell_orders:
            flag = False
            print(order)
        if flag:
            print("暂无卖出")
        print()

    def display_new_trade(self, trade: Trade):
        print("新交易: ")
        print(trade)

    def display_new_order(self, order: Order):
        print("新交易: ")
        print(order)

    def display_trades(self):
        print("所有交易:")
        for trade in self.trades:
            print(trade)


