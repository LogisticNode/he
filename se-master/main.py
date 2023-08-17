import asyncio
import logging
import os
import time

import ccxt.async_support as ccxt

from cli import cli


logger = logging.getLogger()
logger.setLevel(logging.INFO)

logHander = logging.StreamHandler()

formatter = logging.Formatter(
    '[%(asctime)s | %(levelname)s ] %(message)s', 
    datefmt='%Y-%m-%d %H:%M:%S'
)
logHander.setFormatter(formatter)

logger.addHandler(logHander)


if __name__ == '__main__':
    cli(obj={'logger': logger})
