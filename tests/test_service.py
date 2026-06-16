import pytest
from core.poker.service import PokerService
from core.poker.models import SimulationResult

def test_poker_service_analyze_hand_basic():
    # Test with pocket aces vs 1 opponent
    result = PokerService.analyze_hand(
        hole=["As", "Ad"],
        community=["2c", "3h", "4d"],
        num_opponents=1,
        iterations=100
    )
    
    assert isinstance(result, SimulationResult)
    assert result.win_rate > 0.5
    assert "RECOMMENDATION" in result.recommendation
    assert result.equity_iterations == 100

def test_poker_service_incomplete_hand():
    # Pre-flop
    result = PokerService.analyze_hand(
        hole=["As", "Ks"],
        community=[],
        num_opponents=1,
        iterations=100
    )
    
    assert result.hand_name == "Incomplete Hand"
    assert result.win_rate > 0.0

def test_poker_service_full_hand():
    # Royal Flush (manually set up community)
    result = PokerService.analyze_hand(
        hole=["As", "Ks"],
        community=["Qs", "Js", "10s"],
        num_opponents=1,
        iterations=100
    )
    
    assert result.hand_name == "Straight Flush" # 10-A
    assert result.win_rate == 1.0 # Impossible to lose with a Royal Flush
