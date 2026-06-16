from typing import Dict
from .models import SimulationResult

class AdvisoryEngine:
    @staticmethod
    def get_recommendation(win_rate: float) -> str:
        """Determines the semantic recommendation based on win rate."""
        if win_rate > 0.7:
            return "[bold green]RECOMMENDATION: GO ALL-IN / RAISE BIG[/bold green]"
        elif win_rate > 0.4:
            return "[bold yellow]RECOMMENDATION: CALL / VALUE BET[/bold yellow]"
        elif win_rate > 0.2:
            return "[bold blue]RECOMMENDATION: CHECK / SMALL CALL[/bold blue]"
        else:
            return "[bold red]RECOMMENDATION: FOLD[/bold red]"
