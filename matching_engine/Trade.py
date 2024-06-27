"""
Author:  Blank
Date: 2024/6/27
Description:
"""
from .Order import Order


class Trade:
    def __init__(self, buy_order: Order, sell_order: Order, price: int, quantity: int):
        """
        交易类
        :param buy_order: 买入订单
        :param sell_order: 卖出订单
        :param price: 价格
        """
        self.buy_order = buy_order
        self.sell_order = sell_order
        self.price = price
        self.trade_id = -1
        self.quantity = quantity
    def __str__(self):
        return (f"买入订单ID: {self.buy_order.order_id}, 卖出订单ID: {self.sell_order.order_id}, "
                  f"价格: {self.price}, 数量: {self.quantity}")
