from rich.console import Console, Group
from rich.table import Table
from rich.panel import Panel
from rich.columns import Columns
from rich.text import Text
from rich.markdown import Markdown
from typing import List, Dict
from core.poker.models import Card

console = Console()

def render_poker_dashboard(
    player_cards: List[Card], 
    community_cards: List[Card], 
    results: Dict[str, float], 
    hand_name: str,
    recommendation: str
):
    # 1. Cards Section
    hole_display = " ".join([c.rich_repr() for c in player_cards])
    comm_display = " ".join([c.rich_repr() for c in community_cards]) if community_cards else "[italic]Empty[/italic]"
    
    cards_panel = Panel(
        Group(
            f"[bold]Hole Cards:[/bold] {hole_display}",
            f"[bold]Community :[/bold] {comm_display}"
        ),
        title="[bold yellow]Table State[/bold yellow]",
        border_style="bright_blue"
    )

    # 2. Hand Strength
    strength_panel = Panel(
        Text(hand_name, justify="center", style="bold cyan"),
        title="[bold yellow]Current Best Hand[/bold yellow]",
        border_style="bright_blue"
    )

    # 3. Probability Table
    prob_table = Table(show_header=True, header_style="bold magenta", expand=True)
    prob_table.add_column("Outcome", width=12)
    prob_table.add_column("Probability", justify="right")
    
    win_color = "green" if results['win_rate'] > 0.5 else "yellow" if results['win_rate'] > 0.3 else "red"
    
    prob_table.add_row("Win", f"[{win_color}]{results['win_rate']:.2%}[/{win_color}]")
    prob_table.add_row("Tie", f"{results['tie_rate']:.2%}")
    prob_table.add_row("Loss", f"[red]{results['loss_rate']:.2%}[/red]")

    prob_panel = Panel(prob_table, title="[bold yellow]Win Odds[/bold yellow]", border_style="bright_blue")

    # 4. Final Layout
    top_row = Columns([cards_panel, strength_panel], expand=True)
    
    # Recommendation bar
    rec_text = Text.from_markup(recommendation)
    rec_panel = Panel(rec_text, border_style="bright_green", padding=(1, 2))

    return Group(
        top_row,
        prob_panel,
        rec_panel
    )

def render_poker_help():
    """Renders a rich help page for the poker command group."""
    
    # 1. Header & Description
    description = Markdown("""
The Poker Utility provides real-time analysis of Texas Hold'em hands, specifically tuned for **Red Dead Redemption 2**'s NPC behaviors and "Omniscient" AI patterns.
    """)
    
    # 2. Usage Table
    example_table = Table(title="[bold yellow]Usage Examples[/bold yellow]", show_lines=True, expand=True)
    example_table.add_column("Scenario", style="cyan", width=25)
    example_table.add_column("Command", style="green")
    
    example_table.add_row(
        "Pre-Flop Analysis", 
        "rdr2-gambler poker analyze --hole As Kd"
    )
    example_table.add_row(
        "Flop Analysis (3 Opponents)", 
        "rdr2-gambler poker analyze --hole 10s Jh --community 2d 5h 8c --opponents 3"
    )
    example_table.add_row(
        "Exploitative AI Analysis", 
        "rdr2-gambler poker analyze --hole Ad Ah --community Kc --aggression 0.9"
    )
    example_table.add_row(
        "Record & Resolve Hand", 
        "rdr2-gambler poker analyze --hole 8c 9c --record\n"
        "rdr2-gambler poker resolve --id <ID> --outcome win"
    )

    # 3. Parameter Quick-Ref
    param_ref = Table.grid(padding=(0, 2))
    param_ref.add_column(style="bold magenta")
    param_ref.add_column()
    
    param_ref.add_row("--hole", "Input hole cards using shorthand (e.g., 'As', '10h'). Repeat flag for each card.")
    param_ref.add_row("--community", "Input visible community cards (Flop, Turn, River).")
    param_ref.add_row("--opponents", "Number of NPCs at the table (affects win probability).")
    param_ref.add_row("--aggression", "NPC betting intensity (0.0 to 1.0). Higher values weight odds against 'Omniscient' AI.")
    param_ref.add_row("--record", "Persist this hand in the local History database for future calibration.")
    param_ref.add_row("--round-id", "Link this analysis to an existing round (e.g., recording the Turn after the Flop).")

    # 4. Construct the Panel
    help_group = Group(
        description,
        "",
        example_table,
        "",
        Panel(param_ref, title="[bold yellow]Parameter Reference[/bold yellow]", border_style="bright_blue")
    )

    return Panel(help_group, title="[bold cyan]RDR2 Poker Assistant[/bold cyan]", border_style="bright_magenta")
