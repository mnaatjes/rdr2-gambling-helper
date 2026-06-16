import click

@click.group()
def blackjack():
    """Blackjack utility commands."""
    pass

@blackjack.command()
def odds():
    """Calculate current hand odds."""
    click.echo("Calculating Blackjack odds (placeholder)...")
