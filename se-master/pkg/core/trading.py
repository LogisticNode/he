import asyncio
import ccxt.async_support as ccxt
import time

from typing import Dict, Optional
from .meta import CoreABC


class TradingStartedEvent(asyncio.Event):
    pass


class Trading(CoreABC):

    def __init__(self, exchange: ccxt.Exchange):
        self._exchange = exchange


    async def is_trading_started(self, symbol: str, event: TradingStartedEvent, timeout: float) -> bool:
        start_time = time.time()
        while time.time() - start_time < timeout:
            markets = await self._exchange.load_markets(reload=True)

            if symbol in markets:
                await event.set()

            await asyncio.sleep(0.1)


    async def _fetch_order_book(self, symbol: str, side: str, depth=200) -> Dict:
        order_book = await self._exchange.fetch_order_book(symbol, depth)
        orders = None

        if side is None:
            return order_book

        elif side == 'buy':
            orders = order_book['asks']

        else:
            orders = order_book['bids']

        return orders

    @staticmethod
    def _calculate_liquidity(order_book) -> float:
        liquidity = 0

        for price, volume in orders:
            liquidity += price * volume

        return liquidity

    async def calculate_liquidity(self, symbol: str, side: str="", depth: int=500) -> tuple[float, float] | float:
        """
        Calculates liquidity of an specified pair.
        """

        if side == "":
            fetch_buy_orders_task = asyncio.create_task(self._fetch_order_book(self, symbol, 'buy', depth))
            fetch_sell_orders_task = asyncio.create_task(self._fetch_order_book(self, symbol, 'sell', depth))

            buy_orders, sell_orders = await asyncio.gather(fetch_buy_orders_task, fetch_sell_orders_task)

            buy_liquidity = self._calculate_liquidity(buy_orders) 
            sell_liquidity = self._calculate_liquidity(sell_orders)
        
            return buy_liquidity, sell_liquidity

        orders = await self._fetch_order_book(self, symbol, side, depth)
        liquidity = self._calculate_liquidity(orders)

        return liquidity


    async def calculate_price_impact(
        self, 
        symbol: str, 
        side: str, 
        volume: float,
        depth: int
    ) -> float:
        """

        """
        orders = await self._fetch_order_book(self, symbol, side, depth)

        initial_price = orders[0][0]
        remaining_volume = volume

        for price, volume in orders:
            if remaining_volume <= volume:
                last_price = price
                break

            remaining_volume -= volume
        else:
            return -1

        price_impact = ( (last_price - initial_price) / last_price ) * 100
        return price_impact


    async def calculate_trading_volume(
        self,
        pair: Optional[str] = None,
        period: Optional[str] = None, 
    ) -> float:
        ...


    async def order_with_timeout(self, order_data: tuple, timeout: float) -> (bool, tuple[str, str]):
        """
        Cancels an order by its id if it is not filled within a certain time
        :param order_data
        :param timeout
        :returns bool
        :returns tuple[str, str]
        """
        _id, symbol = order_data

        order_status = ""

        start_time = time.time()
        while time.time() - start_time < timeout:
            order_status = await self._exchange.fetch_order_status(_id, symbol)

            if order_status == "closed":
                order_trades = await self._exchange.fetch_order_trades(_id, symbol)
                return True, order_data

            await asyncio.sleep(0.1)

        return False, order_data


    async def order_with_cancel(self, cancel_condition: asyncio.Task[bool, tuple]) -> bool:
        """
        Waits for the completion of the filtering function and, 
        based on the returned data, decides if it's demanded 
        to cancel an order
        
        :param condition: async task that must returns tuple containing order 
        id and its symbol  
        :returns bool: true if an order was filled, false if it was canceled
        """
        success, order_data = await cancel_condition
        _id, symbol = order_data
        
        if success:
            return True

        filled = None
        remaining = None

        try:
            order = await self._exchange.cancel_order(_id, symbol)
        
        except ccxt.OrderNotFound:
            order_status = await self._exchange.fetch_order(_id, symbol)
            if order_status == 'closed':
                return True

        return False


    async def create_order(
        exchange,
        type_: str,
        symbol: str,
        side: str,
        volume: float,
        price: float,
        max_price_impact: float,
        timeout: float
    ):
        """
        
        """
        order = None

        try:
            if type_ == 'limit':
                order = await self._exchange.create_limit_order(symbol, side, volume, price)

            elif type_ == 'market':
                price_impact = await calculate_price_impact(synbol, side, volume, 500)
                if max_price_impact <= price_impact:
                    order = await self._exchange.create_market_order(symbol, side, volume)

                return False
        except:
            return False

        order_data = order['id'], order['symbol']

        order_timeout = asyncio.create_task(order_with_timeout(order_data, timeout))
        ok = await order_with_cancel(self, order_timeout)

        if ok:
            return True

        return False

    async def sell_at_listing():
        await self._exchange.load_markets()
