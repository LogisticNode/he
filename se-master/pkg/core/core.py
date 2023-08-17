import ccxt.async_support as ccxt

from .balance import Balance
from .deposit import Deposit
from .trading import Trading
from .withdraw import Withdraw


class Exchange:
    exchange: ccxt.Exchange
    balance: Balance
    deposit: Deposit
    trading: Trading
    withdraw: Withdraw

    def __init__(
        self, 
        logger, 
        exchange_id: str, 
        api_key: str, 
        secret: str, 
        password=None, 
        proxy=None
    ):
        self.exchange = getattr(ccxt, exchange_id)({
            'apiKey': api_key,
            'secret': secret,
            'password': password,
            'enableRateLimit': True
        })

        self.balance = Balance(self.exchange)
        self.deposit = Deposit(self.exchange)
        self.trading = Trading(self.exchange)
        self.withdraw = Withdraw(self.exchange)
    