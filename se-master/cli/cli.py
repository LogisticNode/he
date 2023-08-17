import asyncio

from typing import (
    Dict
)

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

from pkg.core import Exchange
from pkg.config import Config

from .utils import check_config_file_extention


@group('cli')
@option(
    '-c',
    '--config',
    'config_file',
    type=Path(exists=True),
    default='config.yaml',
    show_default=True,
    help='Location of a config file'
)
@option(
    '-e',
    '--exchange',
    'exchange_name',
    required=False,
    type=Choice(['okx', 'huobi'])
)
@option(
    '--account',
    'account_alias',
    required=False,
    type=str
)
@option(
    '--all',
    'all_accounts',
    required=False,
    type=bool,
    is_flag=True,
    help='Perform an action on all available accounts of all available exchanges.'
)
@pass_context
def cli(ctx: Context, config_file: str, exchange_name: str, account_alias: str, all_accounts: bool):
    config = Config.from_yaml_file(config_file)

    if all_accounts:
        print(config)
        return

    exchange_data = getattr(config, exchange_name)
    if isinstance(exchange_data, Dict):
        try:
            account = exchange_data[account_alias]
        except KeyError:
            # TODO: add logging
            return
        
    account = exchange_data

    logger = None
    if 'logger' in ctx.obj:
        logger = ctx.obj['logger']
    else:
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)

        logHander = logging.StreamHandler()

        formatter = logging.Formatter(
            '[%(asctime)s | %(levelname)s ] %(message)s', 
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        logHander.setFormatter(formatter)

        logger.addHandler(logHander)
    
    exchange = Exchange(
        logger,
        exchange_name, 
        account.api_key, 
        account.secret, 
        account.password, 
        account.proxy
    )

    ctx.obj['exchange'] = exchange
    