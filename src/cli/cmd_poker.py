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
@click.option("--record", is_flag=True, help="Record this hand in history.")
@click.option("--round-id", help="Round ID to associate with (if continuing a hand).")
@click.option("--session-id", help="Explicit Session ID to use.")
def analyze(hole, community, opponents, aggression, record, round_id, session_id):
    """Analyze current poker hand and odds."""
    try:
        from core.poker.service import PokerService
        from core.poker.models import Card
        from .context import CLIContext
        from core.history.service import HistoryService

        # If recording but no session/round provided, check context
        if record and not round_id and not session_id:
            session_id = CLIContext.get_active_session("poker")
            if not session_id:
                # Start new session
                session_id = HistoryService.start_session(game_type="poker")
                CLIContext.set_active_session("poker", session_id)
                console.print(f"[dim]Started new session: [bold white]{session_id}[/bold white][/dim]")

        with console.status("[bold green]Simulating RDR2 game progression..."):
            result = PokerService.analyze_hand(
                hole=list(hole),
                community=list(community),
                num_opponents=opponents,
                aggression=[aggression] * opponents,
                record=record,
                round_id=round_id,
                session_id=session_id
            )

        player_cards = [Card.from_str(c) for c in hole]
        comm_cards = [Card.from_str(c) for c in community]

    except Exception as e:
        console.print(f"[red]Error analyzing hand: {e}[/red]")
        return

    dashboard = render_poker_dashboard(
        player_cards, 
        comm_cards, 
        result.model_dump(), 
        result.hand_name, 
        result.recommendation
    )
    console.print(dashboard)

    if record:
        rid = result.metadata.get("round_id")
        console.print(f"\n[dim]Hand recorded. Round ID: [bold white]{rid}[/bold white][/dim]")
        console.print(f"[dim]Resolve with: [bold cyan]rdr2-gambler poker resolve --id {rid} --outcome win[/bold cyan][/dim]")

@poker.command()
@click.option("--id", required=True, help="The Round ID to resolve.")
@click.option("--outcome", required=True, type=click.Choice(['win', 'loss', 'tie', 'fold']), help="Final outcome of the hand.")
@click.option("--chips", type=int, help="Net chips won or lost.")
def resolve(id, outcome, chips):
    """Resolve a recorded hand with its final outcome."""
    try:
        from core.history.service import HistoryService
        HistoryService.resolve_round(id, outcome, chips)
        console.print(f"[bold green]Round {id} resolved as {outcome.upper()}.[/bold green]")
    except Exception as e:
        console.print(f"[red]Error resolving round: {e}[/red]")
