import sqlite3
from .Order import Order
from .Trade import Trade

class TradingDao:
    def __init__(self, db_name='trading.db'):
        self.conn = sqlite3.connect(db_name)
        self.conn.row_factory = sqlite3.Row
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            order_id INTEGER PRIMARY KEY AUTOINCREMENT,
            order_type TEXT NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL
        )
        ''')

        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS trades (
            trade_id INTEGER PRIMARY KEY AUTOINCREMENT,
            buy_order_id INTEGER NOT NULL,
            sell_order_id INTEGER NOT NULL,
            price REAL NOT NULL,
            quantity INTEGER NOT NULL,
            FOREIGN KEY (buy_order_id) REFERENCES orders (order_id),
            FOREIGN KEY (sell_order_id) REFERENCES orders (order_id)
        )
        ''')

        self.conn.commit()

    def insert_order(self, order):
        self.cursor.execute('''
        INSERT INTO orders (order_type, price, quantity)
        VALUES (?, ?, ?)
        ''', (order.order_type, order.price, order.quantity))
        self.conn.commit()
        order.order_id = self.cursor.lastrowid  # 获取自增ID
        return order

    def get_order(self, order_id):
        self.cursor.execute('SELECT * FROM orders WHERE order_id = ?', (order_id,))
        row = self.cursor.fetchone()
        if row:
            return Order(row['order_type'], row['price'], row['quantity'], row['order_id'])

        return None

    def get_all_orders(self, status='all'):
        """

        :param status: 三个状态 completed uncompleted all
        :return: Orders: List[Order]
        """
        if status == 'completed':
            self.cursor.execute('''
            SELECT * FROM orders WHERE quantity = 0
            ''')
        elif status == 'uncompleted':
            self.cursor.execute('''
            SELECT * FROM orders WHERE quantity > 0
            ''')
        else:  # status == 'all'
            self.cursor.execute('SELECT * FROM orders')

        rows = self.cursor.fetchall()
        return [Order(row['price'], row['order_type'], row['quantity'], row['order_id']) for row in rows]

    def update_order(self, order):
        self.cursor.execute('''
        UPDATE orders
        SET order_type = ?, price = ?, quantity = ?
        WHERE order_id = ?
        ''', (order.order_type, order.price, order.quantity, order.order_id))
        self.conn.commit()

    def delete_order(self, order_id):
        self.cursor.execute('DELETE FROM orders WHERE order_id = ?', (order_id,))
        self.conn.commit()

    def insert_trade(self, trade):
        self.cursor.execute('''
        INSERT INTO trades (buy_order_id, sell_order_id, price, quantity)
        VALUES (?, ?, ?, ?)
        ''', (trade.buy_order.order_id, trade.sell_order.order_id, trade.price, trade.quantity))
        self.conn.commit()
        trade.trade_id = self.cursor.lastrowid  # 获取自增ID
        return trade

    def get_trade(self, trade_id):
        self.cursor.execute('SELECT * FROM trades WHERE trade_id = ?', (trade_id,))
        row = self.cursor.fetchone()
        if row:
            buy_order = self.get_order(row['buy_order_id'])
            sell_order = self.get_order(row['sell_order_id'])
            return Trade(buy_order, sell_order, row['price'], row['quantity'], row['trade_id'])
        return None

    def get_all_trades(self):
        self.cursor.execute('SELECT * FROM trades')
        rows = self.cursor.fetchall()
        trades = []
        for row in rows:
            buy_order = self.get_order(row['buy_order_id'])
            sell_order = self.get_order(row['sell_order_id'])
            trades.append(Trade(buy_order, sell_order, row['price'], row['quantity'], row['trade_id']))
        return trades

    def update_trade(self, trade):
        self.cursor.execute('''
        UPDATE trades
        SET buy_order_id = ?, sell_order_id = ?, price = ?, quantity = ?
        WHERE trade_id = ?
        ''', (trade.buy_order.order_id, trade.sell_order.order_id, trade.price, trade.quantity, trade.trade_id))
        self.conn.commit()

    def delete_trade(self, trade_id):
        self.cursor.execute('DELETE FROM trades WHERE trade_id = ?', (trade_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()