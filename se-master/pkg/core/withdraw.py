import ccxt.async_support as ccxt

from .meta import CoreABC


class Withdraw(CoreABC):
    
    def __init__(self, exchange: ccxt.Exchange):
        self._exchange = exchange
        