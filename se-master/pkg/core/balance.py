import asyncio

import ccxt.async_support as ccxt

from .meta import CoreABC


class Balance(CoreABC):

    def __init__(self, exchange: ccxt.Exchange):
        self._exchange = exchange
    
    async def show_balance(self):
        balance = await self._exchange.fetch_balance()
        print(balance)