import click
from rich.console import Console
from core.poker.models import Card
from core.poker.evaluator import Evaluator
from core.poker.predictive import RDR2Predictive
from ui.renderers import render_poker_dashboard, render_poker_help

console = Console()

class PokerGroup(click.Group):
    def format_help(self, ctx, formatter):
        # Intercept --help and show our Rich dashboard instead
        console.print(render_poker_help())

@click.group(cls=PokerGroup)
def poker():
    """Poker utility commands."""
    pass

@poker.command()
@click.option("--hole", multiple=True, required=True, help="Your hole cards (e.g. As Kd)")
@click.option("--community", multiple=True, help="Visible community cards")
@click.option("--opponents", default=1, help="Number of opponents")
@click.option("--aggression", default=0.2, help="General NPC aggression level (0.0 - 1.0)")
def analyze(hole, community, opponents, aggression):
    """Analyze current poker hand and odds."""
    try:
        # Use the Service Layer instead of orchestrating here
        from core.poker.service import PokerService
        from core.poker.models import Card

        with console.status("[bold green]Simulating RDR2 game progression..."):
            result = PokerService.analyze_hand(
                hole=list(hole),
                community=list(community),
                num_opponents=opponents,
                aggression=[aggression] * opponents
            )

        # Parse cards for rendering (Service returns raw data, UI needs objects)
        player_cards = [Card.from_str(c) for c in hole]
        comm_cards = [Card.from_str(c) for c in community]

    except Exception as e:
        console.print(f"[red]Error analyzing hand: {e}[/red]")
        return

    # Render the enhanced dashboard using the standardized result object
    dashboard = render_poker_dashboard(
        player_cards, 
        comm_cards, 
        result.dict(), # Convert Pydantic to dict for renderer compatibility
        result.hand_name, 
        result.recommendation
    )
    console.print(dashboard)
