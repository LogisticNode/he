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

@group('cli')
@pass_context
def cli(ctx: Context):
    accounts = load_accounts_from_file('kucoin')
    ctx.obj['accounts'] = accounts


@cli.command(
    'internal-transfer',
    help='transfer tokens between internal accounts'
)
@option(
    '--token',
    '-tn',
    required=True,
    type=str,
    help='Token ticker to transfer'
)
@option(
    '--amount',
    '-am',
    required=False,
    type=float,
    help='Number of tokens to transfer'
)
@option(
    '--direction',
    '-d',
    required=False,
    type=Choice(['main->trade', 'trade->main']),
    default='main->trade',
    show_default=True,
    help='Specify an internal account for transfer and receipt'
)
@pass_context
def internal_transfer(ctx: Context, token: str, direction: str):
    ...