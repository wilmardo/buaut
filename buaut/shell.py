import pbr.version
import socket
import click

from buaut import command
from bunq.sdk.context import ApiContext, BunqContext, ApiEnvironmentType

@click.group()
@click.option(
    '--iban',
    envvar='BUAUT_IBAN',
    required=True,
    help='Enter IBAN where to run a function. '
          'Can be set as environment variable BUAUT_IBAN',
    type=click.STRING
)
@click.option(
    '--api-key',
    envvar='BUAUT_API_KEY',
    required=True,
    help='Provide the api token for the Bunq API. '
          'Can be set as environment variable BUAUT_API_KEY',
    type=click.STRING
)
@click.option(
    '--sandbox',
    envvar='BUAUT_SANDBOX',
    is_flag=True,
    help='Pass when testing against the Bunq sandbox. '
          'Can be set as environment variable BUAUT_IBAN',
)
@click.version_option(version=pbr.version.VersionInfo('buaut'))
@click.pass_context
def main(ctx, sandbox, iban, api_key):
    """
    \b
     ____                    _
    | __ ) _   _  __ _ _   _| |_
    |  _ \| | | |/ _` | | | | __|
    | |_) | |_| | (_| | |_| | |_
    |____/ \__,_|\__,_|\__,_|\__|

    Buaut are several Bunq automations in a
    convenient CLI tool.

    Enable autocomplete for Bash (.bashrc):
      eval "$(_BUAUT_COMPLETE=source buaut)"

    Enable autocomplete for ZSH (.zshrc):
      eval "$(_BUAUT_COMPLETE=source_zsh buaut)"
    """
    ctx.obj = {}
    ctx.obj['args'] = {}
    ctx.obj['args']['iban'] = iban
    ctx.obj['args']['api_key'] = api_key

    # Set Bunq context
    context = ApiEnvironmentType.SANDBOX if sandbox \
              else ApiEnvironmentType.PRODUCTION

    # Setup Bunq authentication
    api_context = ApiContext(context, api_key,
      socket.gethostname())
    api_context.ensure_session_active()

    # Load api context into BunqContext used for subsequent calls
    BunqContext.load_api_context(api_context)

main.add_command(command.request.request)