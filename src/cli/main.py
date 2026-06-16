import click
from .cmd_blackjack import blackjack
from .cmd_poker import poker
from .cmd_history import history

@click.group()
@click.option("-v", "--verbose", is_flag=True, help="Enable verbose logging.")
@click.version_option(version="0.1.0", prog_name="rdr2-gambler")
def cli(verbose: bool):
    """Red Dead Redemption 2 Gambling Utility."""
    if verbose:
        click.echo("Verbose mode enabled.", err=True)

# Register subcommands
cli.add_command(blackjack)
cli.add_command(poker)
cli.add_command(history)
