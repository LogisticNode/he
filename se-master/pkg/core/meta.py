import ccxt.async_support as ccxt
from abc import ABC


class CoreABC(ABC):
    _ccxt: ccxt.Exchange
