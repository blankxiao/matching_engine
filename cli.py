"""
Author:  Blank
Date: 2024/6/27
Description: 
"""


import click
from matching_engine.TradingDao import TradingDao
from matching_engine.OrderBook import OrderBook
from matching_engine.Order import Order


@click.group()
@click.pass_context
def cli(ctx):
    ctx.ensure_object(dict)
    ctx.obj['db'] = TradingDao()  # 初始化数据库连接
    ctx.obj['order_book'] = OrderBook(ctx.obj['db'])  # 初始化订单簿

@cli.command()
@click.pass_context
@click.option('--price', type=int, required=True, help='Order price')
@click.option('--order_type', type=click.Choice(['buy', 'sell']), required=True, help='Order type')
@click.option('--quantity', type=int, required=True, help='Order quantity')
def add_order(ctx, price, order_type, quantity):
    """添加新订单"""
    order = Order(price=price, order_type=order_type, quantity=quantity)
    ctx.obj['order_book'].add_order(order)
    click.echo("成功添加！")
    ctx.obj['order_book'].display_order_book()

@cli.command()
@click.pass_context
def display_order_book(ctx):
    """显示当前的所有订单"""
    ctx.obj['order_book'].display_order_book()

@cli.command()
@click.pass_context
def display_trades(ctx):
    """显示当前的所有交易"""
    ctx.obj['order_book'].display_trades()

@cli.command()
@click.pass_context
def match_orders(ctx):
    """开始撮合交易"""
    ctx.obj['order_book'].match_orders()
    click.echo("交易完成.")
    ctx.obj['order_book'].display_order_book()
    ctx.obj['order_book'].display_trades()

if __name__ == '__main__':
    cli()