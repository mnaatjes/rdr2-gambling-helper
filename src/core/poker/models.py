from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import List, Optional
import random
from enum import IntEnum

class Suit(IntEnum):
    CLUBS = 0
    DIAMONDS = 1
    HEARTS = 2
    SPADES = 3

    def __str__(self):
        return self.name[0].lower()

class Rank(IntEnum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14

    def __str__(self):
        if self <= 10:
            return str(self.value)
        return self.name[0]

class Card(BaseModel):
    model_config = ConfigDict(frozen=True)
    rank: Rank
    suit: Suit

    @classmethod
    def from_str(cls, s: str) -> 'Card':
        suit_map = {'c': Suit.CLUBS, 'd': Suit.DIAMONDS, 'h': Suit.HEARTS, 's': Suit.SPADES}
        rank_map = {
            '2': Rank.TWO, '3': Rank.THREE, '4': Rank.FOUR, '5': Rank.FIVE,
            '6': Rank.SIX, '7': Rank.SEVEN, '8': Rank.EIGHT, '9': Rank.NINE,
            '10': Rank.TEN, 'J': Rank.JACK, 'Q': Rank.QUEEN, 'K': Rank.KING, 'A': Rank.ACE,
            'j': Rank.JACK, 'q': Rank.QUEEN, 'k': Rank.KING, 'a': Rank.ACE
        }
        
        if len(s) == 3: # "10s"
            r_str = s[:2]
            s_str = s[2].lower()
        else:
            r_str = s[0]
            s_str = s[1].lower()
            
        return cls(rank=rank_map[r_str], suit=suit_map[s_str])

    def __repr__(self):
        return f"{str(self.rank)}{str(self.suit)}"

    def __str__(self):
        return self.__repr__()

    def rich_repr(self):
        suit_colors = {
            Suit.CLUBS: "white",
            Suit.DIAMONDS: "red",
            Suit.HEARTS: "red",
            Suit.SPADES: "white"
        }
        suit_symbols = {
            Suit.CLUBS: "♣",
            Suit.DIAMONDS: "♦",
            Suit.HEARTS: "♥",
            Suit.SPADES: "♠"
        }
        color = suit_colors[self.suit]
        symbol = suit_symbols[self.suit]
        return f"[{color}]{self.rank}{symbol}[/{color}]"

class GameState(BaseModel):
    hole_cards: List[Card]
    community_cards: List[Card] = Field(default_factory=list)
    num_opponents: int = 1
    npc_aggression: List[float] = Field(default_factory=list)

    @field_validator('npc_aggression', mode='before')
    @classmethod
    def set_default_aggression(cls, v, info):
        if not v:
            # Note: num_opponents might not be in info.data yet if it's being validated
            # But we can default it or handle it in service.
            return [] 
        return v

class SimulationResult(BaseModel):
    win_rate: float
    tie_rate: float
    loss_rate: float
    hand_name: str
    recommendation: str
    equity_iterations: int

class Deck:
    def __init__(self):
        self.cards = [Card(rank=r, suit=s) for r in Rank for s in Suit]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self, n: int = 1) -> List[Card]:
        return [self.cards.pop() for _ in range(n)]

    def remove(self, card: Card):
        if card in self.cards:
            self.cards.remove(card)
