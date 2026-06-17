from typing import Dict
from .models import SimulationResult

class AdvisoryEngine:
    @staticmethod
    def get_recommendation(win_rate: float) -> str:
        """Determines the semantic recommendation based on win rate."""
        if win_rate > 0.7:
            return "GO ALL-IN / RAISE BIG"
        elif win_rate > 0.4:
            return "CALL / VALUE BET"
        elif win_rate > 0.2:
            return "CHECK / SMALL CALL"
        else:
            return "FOLD"
