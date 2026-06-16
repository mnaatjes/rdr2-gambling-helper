import random
from typing import List, Dict
from .models import Card, Deck
from .evaluator import Evaluator

class PokerEngine:
    @staticmethod
    def calculate_equity(player_hand: List[Card], community_cards: List[Card], num_opponents: int, iterations: int = 1000) -> Dict[str, float]:
        wins = 0
        ties = 0
        losses = 0

        for _ in range(iterations):
            deck = Deck()
            # Remove known cards from deck
            for c in player_hand:
                deck.remove(c)
            for c in community_cards:
                deck.remove(c)
            
            # Draw remaining community cards
            remaining_community = deck.draw(5 - len(community_cards))
            full_community = community_cards + remaining_community
            
            # Draw opponent hands
            opponent_hands = []
            for _ in range(num_opponents):
                opponent_hands.append(deck.draw(2))
            
            player_rank = Evaluator.evaluate_7_cards(player_hand + full_community)
            
            best_opponent_rank = None
            for opp_hand in opponent_hands:
                opp_rank = Evaluator.evaluate_7_cards(opp_hand + full_community)
                if best_opponent_rank is None or opp_rank > best_opponent_rank:
                    best_opponent_rank = opp_rank
            
            if player_rank > best_opponent_rank:
                wins += 1
            elif player_rank == best_opponent_rank:
                ties += 1
            else:
                losses += 1

        total = iterations
        return {
            "win_rate": wins / total,
            "tie_rate": ties / total,
            "loss_rate": losses / total
        }
