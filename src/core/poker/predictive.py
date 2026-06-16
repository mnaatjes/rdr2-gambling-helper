from typing import List, Dict
from .models import Card, Deck
from .evaluator import Evaluator, HandRank

class RDR2Predictive:
    @staticmethod
    def adjust_for_npc_behavior(player_hand: List[Card], community_cards: List[Card], 
                               npc_aggression: List[float], iterations: int = 1000) -> Dict[str, float]:
        """
        Adjusts equity calculations based on NPC betting behavior.
        npc_aggression: a list of floats (0 to 1) representing how aggressive each NPC is being.
        """
        wins = 0
        ties = 0
        losses = 0
        total_valid_sims = 0

        # This mimics the "Omniscient AI" by assuming aggressive NPCs are more likely
        # to be in simulations where they end up with strong hands.
        
        while total_valid_sims < iterations:
            deck = Deck()
            for c in player_hand: deck.remove(c)
            for c in community_cards: deck.remove(c)
            
            remaining_community = deck.draw(5 - len(community_cards))
            full_community = community_cards + remaining_community
            
            opponent_hands = [deck.draw(2) for _ in npc_aggression]
            
            # Evaluate everyone
            player_rank = Evaluator.evaluate_7_cards(player_hand + full_community)
            opp_ranks = [Evaluator.evaluate_7_cards(h + full_community) for h in opponent_hands]
            
            # "RDR2 Omniscience Filter"
            # If an NPC is aggressive (e.g. 0.8), and their final hand is weak (e.g. High Card),
            # we consider this simulation less "likely" in the RDR2 engine's pre-determined world.
            
            is_valid_sim = True
            for i, agg in enumerate(npc_aggression):
                if agg > 0.6 and opp_ranks[i].rank_type < 2: # Aggressive but only has High Card
                    # In RDR2, an aggressive NPC almost certainly has at least a pair by the river
                    if i % 2 == 0: # Add some randomness to the filter
                        is_valid_sim = False
                        break
            
            if not is_valid_sim:
                continue
                
            best_opponent_rank = max(opp_ranks)
            
            if player_rank > best_opponent_rank:
                wins += 1
            elif player_rank == best_opponent_rank:
                ties += 1
            else:
                losses += 1
            
            total_valid_sims += 1

        return {
            "win_rate": wins / iterations,
            "tie_rate": ties / iterations,
            "loss_rate": losses / iterations
        }
