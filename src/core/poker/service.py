from typing import List, Optional, Union, Dict, Any
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
        iterations: int = 2000,
        record: bool = False,
        round_id: Optional[str] = None,
        **kwargs
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
        elif len(all_cards) == 2:
            c1, c2 = player_cards
            if c1.rank == c2.rank:
                hand_name = f"Pocket {c1.rank.name.capitalize()}s"
            else:
                high_card = c1 if c1.rank > c2.rank else c2
                hand_name = f"{high_card.rank.name.capitalize()} High"
        else:
            hand_name = "Waiting for Board..."
            
        # 4. Get Recommendation
        recommendation = AdvisoryEngine.get_recommendation(results['win_rate'])
        
        sim_result = SimulationResult(
            win_rate=results['win_rate'],
            tie_rate=results['tie_rate'],
            loss_rate=results['loss_rate'],
            hand_name=hand_name,
            recommendation=recommendation,
            equity_iterations=iterations
        )

        # 5. Optional Telemetry (Service B Integration)
        if record:
            from core.history.service import HistoryService
            
            # If we don't have a round_id but we have a session_id, start a new round
            if not round_id:
                session_id = kwargs.get('session_id')
                if not session_id:
                    session_id = HistoryService.start_session(game_type="poker")
                
                round_id = HistoryService.start_round(session_id)
            
            uhh_state = {
                "meta": {"version": "1.0", "game": "poker"},
                "state": {
                    "hole": [str(c) for c in player_cards],
                    "community": [str(c) for c in comm_cards],
                    "opponents": num_opponents,
                    "context": {"aggression": npc_agg}
                }
            }
            
            HistoryService.record_snapshot(round_id, uhh_state, sim_result.model_dump())
            sim_result.metadata = {"round_id": round_id}

        return sim_result
