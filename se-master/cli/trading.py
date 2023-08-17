from click import (
    argument,
    command,
    group,
    pass_context,
    option,
    Context,
    Choice,
    Option,
    Path
)

from .cli import cli
from .types import Alias


@cli.command('spot-trade')
@option(
    '-a',
    '--action',
    required=True,
    type=Choice(['buy', 'sell']),
    help='Side of an created order.'
)
@option(
    '--pair',
    'pair',
    required=True,
    type=str,
    help='Trading pair in which the action will be performed.'
)
@option(
    '--price',
    type=float,
    help='Price at which the tokens will be sold.'
)
@option(
    '-pI',
    '--max-price-impact',
    default=0.1,
    show_default=True,
    help='Maximum acceptable impact of an order to the price.'
)
@option(
    '-a',
    '--amount',
    required=True,
    type=float,
    help='Amount of tokens to be sold.'
)
@option(
    '-oT',
    '--order-type',
    'order_type',
    type=Choice(['limit', 'market']),
    default='limit',
    show_default=True,
    help='Type of an order to be created. Available types: limit, market.'
)
@option(
    '-t',
    '--timeout',
    type=float,
    default=20,
    show_default=True,
    help='Period of time in seconds after which an order will be cancelled if it was not filled.'
)
@option(
    '-w',
    '--watch-listing',
    type=bool,
    is_flag=True,
    default=False,
    show_default=True,
    help='Check whether trading has started and create an order immediately after the start of trading.'
)
@pass_context
def spot_trade(
    ctx: Context,
    watch_listing: str,
    exchange_name: str,
    action: str, 
    pair: str, 
    price: float, 
    amount: float, 
    order_type: str, 
    max_price_impact: float, 
    timeout: float,
    watch_listing: bool
):
    exchange = ctx.obj['exchange']
        

    asyncio.run(
        exchange.trading.create_order(
        order_type, 
        pair, 
        side, 
        volume, 
        price, 
        max_price_impact, 
        timeout
    ))

@cli.command('market-data')
@pass_context
def market_data(
    ctx: Context,
    exchange_name: str,
    action: str, 
    pair: str, 
    price: float, 
    amount: float, 
    order_type: str, 
    max_price_impact: float, 
    timeout: float
):
    exchange = ctx.obj['exchange']

    asyncio.run(
        exchange.trading.create_order(
        order_type, 
        pair, 
        side, 
        volume, 
        price, 
        max_price_impact, 
        timeout
    ))
