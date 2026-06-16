from core.poker.models import Card, Rank, Suit, Deck
from core.poker.evaluator import Evaluator
from core.poker.engine import PokerEngine

def test_card_from_str():
    c = Card.from_str("As")
    assert c.rank == Rank.ACE
    assert c.suit == Suit.SPADES
    
    c2 = Card.from_str("10h")
    assert c2.rank == Rank.TEN
    assert c2.suit == Suit.HEARTS

def test_hand_evaluation_flush():
    cards = [
        Card(rank=Rank.ACE, suit=Suit.SPADES),
        Card(rank=Rank.TEN, suit=Suit.SPADES),
        Card(rank=Rank.TWO, suit=Suit.SPADES),
        Card(rank=Rank.FIVE, suit=Suit.SPADES),
        Card(rank=Rank.SEVEN, suit=Suit.SPADES)
    ]
    rank = Evaluator.evaluate_5_cards(cards)
    assert rank.rank_type == 6 # Flush
    assert Evaluator.rank_to_name(rank.rank_type) == "Flush"

def test_hand_evaluation_full_house():
    cards = [
        Card(rank=Rank.ACE, suit=Suit.SPADES),
        Card(rank=Rank.ACE, suit=Suit.HEARTS),
        Card(rank=Rank.ACE, suit=Suit.CLUBS),
        Card(rank=Rank.TEN, suit=Suit.SPADES),
        Card(rank=Rank.TEN, suit=Suit.HEARTS)
    ]
    rank = Evaluator.evaluate_5_cards(cards)
    assert rank.rank_type == 7 # Full House

def test_poker_equity():
    hole = [Card.from_str("As"), Card.from_str("Ad")]
    community = [Card.from_str("2c"), Card.from_str("3h"), Card.from_str("4d")]
    results = PokerEngine.calculate_equity(hole, community, num_opponents=1, iterations=100)
    # Pocket Aces against 1 opponent on a dry board should have high win rate
    assert results["win_rate"] > 0.5
