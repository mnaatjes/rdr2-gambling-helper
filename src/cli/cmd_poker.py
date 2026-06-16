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
        player_cards = [Card.from_str(c) for c in hole]
        comm_cards = [Card.from_str(c) for c in community]
    except Exception as e:
        console.print(f"[red]Error parsing cards: {e}[/red]")
        return

    # Calculate base odds
    with console.status("[bold green]Simulating RDR2 game progression..."):
        results = RDR2Predictive.adjust_for_npc_behavior(
            player_cards, comm_cards, [aggression] * opponents, iterations=2000
        )

    # Current hand strength
    all_cards = player_cards + comm_cards
    if len(all_cards) >= 5:
        rank = Evaluator.evaluate_7_cards(all_cards)
        hand_name = Evaluator.rank_to_name(rank.rank_type)
    else:
        hand_name = "Incomplete Hand"

    # Recommendation
    win_rate = results['win_rate']
    if win_rate > 0.7:
        rec = "[bold green]RECOMMENDATION: GO ALL-IN / RAISE BIG[/bold green]"
    elif win_rate > 0.4:
        rec = "[bold yellow]RECOMMENDATION: CALL / VALUE BET[/bold yellow]"
    elif win_rate > 0.2:
        rec = "[bold blue]RECOMMENDATION: CHECK / SMALL CALL[/bold blue]"
    else:
        rec = "[bold red]RECOMMENDATION: FOLD[/bold red]"
    
    # Render the enhanced dashboard
    dashboard = render_poker_dashboard(
        player_cards, comm_cards, results, hand_name, rec
    )
    console.print(dashboard)
