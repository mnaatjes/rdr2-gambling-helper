import click
from rich.console import Console
from rich.table import Table
from core.history.service import HistoryService
import json

console = Console()

@click.group()
def history():
    """View and manage gambling history."""
    pass

@history.command(name="list")
@click.option("--limit", default=10, help="Number of sessions to show.")
def list_sessions(limit):
    """List recent gambling sessions."""
    db = HistoryService.get_db()
    with db._get_connection() as conn:
        sessions = conn.execute(
            "SELECT session_id, game_type, location, start_time FROM sessions ORDER BY start_time DESC LIMIT ?",
            (limit,)
        ).fetchall()

    if not sessions:
        console.print("[yellow]No history found.[/yellow]")
        return

    table = Table(title="Recent Sessions")
    table.add_column("ID", style="dim", width=14)
    table.add_column("Game", style="cyan")
    table.add_column("Location", style="green")
    table.add_column("Started")

    for s in sessions:
        table.add_row(*[str(i) for i in s])
    
    console.print(table)

@history.command(name="rounds")
@click.option("--session-id", help="Filter by session ID.")
@click.option("--limit", default=10, help="Number of rounds to show.")
def list_rounds(session_id, limit):
    """List recent game rounds."""
    db = HistoryService.get_db()
    query = "SELECT round_id, session_id, timestamp, final_outcome, net_chips FROM rounds"
    params = []
    
    if session_id:
        query += " WHERE session_id = ?"
        params.append(session_id)
    
    query += " ORDER BY timestamp DESC LIMIT ?"
    params.append(limit)

    with db._get_connection() as conn:
        rounds = conn.execute(query, tuple(params)).fetchall()

    if not rounds:
        console.print("[yellow]No rounds found.[/yellow]")
        return

    table = Table(title="Recent Rounds")
    table.add_column("Round ID", style="dim", width=14)
    table.add_column("Outcome", style="bold")
    table.add_column("Chips", justify="right")
    table.add_column("Timestamp")

    for r in rounds:
        outcome = r[3] or "PENDING"
        color = "green" if outcome == "win" else "red" if outcome == "loss" else "yellow"
        chips = f"{r[4]:+d}" if r[4] is not None else "-"
        table.add_row(r[0], f"[{color}]{outcome}[/{color}]", chips, r[2])
    
    console.print(table)

@history.command()
@click.argument("game_type", type=click.Choice(['poker', 'blackjack']))
@click.option("--location", help="Game location.")
def start(game_type, location):
    """Manually start a new gambling session."""
    from .context import CLIContext
    session_id = HistoryService.start_session(game_type, location)
    CLIContext.set_active_session(game_type, session_id)
    console.print(f"[bold green]Started new {game_type} session: {session_id}[/bold green]")

@history.command()
@click.argument("game_type", type=click.Choice(['poker', 'blackjack']))
def stop(game_type):
    """Stop the active session for a game type."""
    from .context import CLIContext
    CLIContext.clear_session(game_type)
    console.print(f"[bold yellow]Active {game_type} session cleared.[/bold yellow]")

@history.command(name="inspect")
@click.argument("round_id")
def inspect_round(round_id):
    """View detailed snapshots for a specific round."""
    db = HistoryService.get_db()
    with db._get_connection() as conn:
        snapshots = conn.execute(
            "SELECT snapshot_id, game_state_json, prediction_json, timestamp FROM snapshots WHERE round_id = ? ORDER BY timestamp ASC",
            (round_id,)
        ).fetchall()

    if not snapshots:
        console.print(f"[yellow]No snapshots found for round {round_id}.[/yellow]")
        return

    console.print(f"\n[bold cyan]Inspection: Round {round_id}[/bold cyan]\n")
    
    for i, s in enumerate(snapshots):
        state = json.loads(s[1])
        pred = json.loads(s[2])
        
        table = Table(title=f"Snapshot {i+1} ({s[3]})", expand=True)
        table.add_column("Game State", ratio=1)
        table.add_column("Prediction", ratio=1)
        
        # Format the JSONs for better viewing
        state_str = json.dumps(state.get('state', {}), indent=2)
        pred_str = json.dumps({k: v for k, v in pred.items() if k != 'metadata'}, indent=2)
        
        table.add_row(state_str, pred_str)
        console.print(table)
        console.print("")
