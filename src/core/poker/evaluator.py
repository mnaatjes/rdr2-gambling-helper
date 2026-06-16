from typing import List, Tuple
from collections import Counter
from itertools import combinations
from functools import total_ordering
from .models import Card, Rank, Suit

@total_ordering
class HandRank:
    def __init__(self, rank_type: int, values: List[int]):
        self.rank_type = rank_type
        self.values = values

    def __lt__(self, other):
        if self.rank_type != other.rank_type:
            return self.rank_type < other.rank_type
        return self.values < other.values

    def __eq__(self, other):
        return self.rank_type == other.rank_type and self.values == other.values

class Evaluator:
    @staticmethod
    def evaluate_5_cards(cards: List[Card]) -> HandRank:
        ranks = sorted([c.rank.value for c in cards], reverse=True)
        suits = [c.suit for c in cards]
        is_flush = len(set(suits)) == 1
        
        # Check for straight
        is_straight = False
        if len(set(ranks)) == 5:
            if ranks[0] - ranks[4] == 4:
                is_straight = True
            elif ranks == [14, 5, 4, 3, 2]: # A-5 Straight
                is_straight = True
                ranks = [5, 4, 3, 2, 1]

        counts = Counter(ranks)
        mc = counts.most_common()
        
        # Straight Flush
        if is_flush and is_straight:
            return HandRank(9, ranks)
        
        # Four of a Kind
        if mc[0][1] == 4:
            return HandRank(8, [mc[0][0], mc[1][0]])
        
        # Full House
        if mc[0][1] == 3 and mc[1][1] == 2:
            return HandRank(7, [mc[0][0], mc[1][0]])
        
        # Flush
        if is_flush:
            return HandRank(6, ranks)
        
        # Straight
        if is_straight:
            return HandRank(5, ranks)
        
        # Three of a Kind
        if mc[0][1] == 3:
            return HandRank(4, [mc[0][0], mc[1][0], mc[2][0]])
        
        # Two Pair
        if mc[0][1] == 2 and mc[1][1] == 2:
            return HandRank(3, sorted([mc[0][0], mc[1][0]], reverse=True) + [mc[2][0]])
        
        # One Pair
        if mc[0][1] == 2:
            return HandRank(2, [mc[0][0]] + sorted([mc[1][0], mc[2][0], mc[3][0]], reverse=True))
        
        # High Card
        return HandRank(1, ranks)

    @classmethod
    def evaluate_7_cards(cls, cards: List[Card]) -> HandRank:
        best_rank = HandRank(0, [])
        for combo in combinations(cards, 5):
            rank = cls.evaluate_5_cards(list(combo))
            if rank > best_rank:
                best_rank = rank
        return best_rank

    @staticmethod
    def rank_to_name(rank_type: int) -> str:
        names = {
            9: "Straight Flush",
            8: "Four of a Kind",
            7: "Full House",
            6: "Flush",
            5: "Straight",
            4: "Three of a Kind",
            3: "Two Pair",
            2: "One Pair",
            1: "High Card"
        }
        return names.get(rank_type, "Unknown")
