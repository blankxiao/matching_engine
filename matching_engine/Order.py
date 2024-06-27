"""
Author:  Blank
Date: 2024/6/27
Description:
"""
class Order:
    def __init__(self, price: int, order_type: str, quantity: int, order_id=-1):
        """
        订单类
        :param order_id: 订单id
        :param order_type: 订单类型 buy or sell
        :param price: 价格
        :param quantity: 数量
        """
        self.order_id = order_id
        self.order_type = order_type
        self.price = price
        self.quantity = quantity
    def __str__(self):
        return (f"类型: {'卖出' if self.order_type == 'sell' else '买入'}, 价格: {self.price}, 数量: {self.quantity}, ID: {self.order_id}, ")
