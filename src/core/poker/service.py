from typing import List, Optional, Union
from .models import Card, GameState, SimulationResult
from .predictive import RDR2Predictive
from .evaluator import Evaluator
from .advisory import AdvisoryEngine

class PokerService:
    @staticmethod
    def analyze_hand(
        hole: Union[List[str], List[Card]], 
        community: Optional[Union[List[str], List[Card]]] = None, 
        num_opponents: int = 1,
        aggression: Optional[List[float]] = None,
        iterations: int = 2000
    ) -> SimulationResult:
        """
        High-level API for analyzing a poker hand.
        Orchestrates simulation, evaluation, and recommendation.
        """
        # 1. Parse Input
        player_cards = [Card.from_str(c) if isinstance(c, str) else c for c in hole]
        comm_cards = [Card.from_str(c) if isinstance(c, str) else c for c in (community or [])]
        
        npc_agg = aggression or ([0.2] * num_opponents)
        
        # 2. Run Simulation
        results = RDR2Predictive.adjust_for_npc_behavior(
            player_cards, comm_cards, npc_agg, iterations=iterations
        )
        
        # 3. Determine Hand Strength
        all_cards = player_cards + comm_cards
        if len(all_cards) >= 5:
            rank = Evaluator.evaluate_7_cards(all_cards)
            hand_name = Evaluator.rank_to_name(rank.rank_type)
        else:
            hand_name = "Incomplete Hand"
            
        # 4. Get Recommendation
        recommendation = AdvisoryEngine.get_recommendation(results['win_rate'])
        
        return SimulationResult(
            win_rate=results['win_rate'],
            tie_rate=results['tie_rate'],
            loss_rate=results['loss_rate'],
            hand_name=hand_name,
            recommendation=recommendation,
            equity_iterations=iterations
        )
