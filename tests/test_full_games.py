import pytest
import sqlite3
import json
from core.poker.service import PokerService
from core.history.service import HistoryService
from core.history.db import HistoryDB

@pytest.fixture
def test_env(tmp_path):
    # Setup temporary DB
    db_path = tmp_path / "full_game_test.db"
    original_db = HistoryService._db
    HistoryService._db = HistoryDB(db_path=db_path)
    yield HistoryService._db
    HistoryService._db = original_db

def test_two_full_games(test_env):
    # --- GAME 1: WINNING STRAIGHT ---
    # 1. Start Session
    sid = HistoryService.start_session(game_type="poker", location="Saint_Denis")
    assert len(sid) == 12
    
    # 2. Round 1: Pre-Flop
    # No round_id yet, so we pass session_id
    res1 = PokerService.analyze_hand(hole=["As", "Kd"], record=True, session_id=sid)
    rid1 = res1.metadata["round_id"]
    assert len(rid1) == 12
    
    # 3. Round 1: Flop
    res2 = PokerService.analyze_hand(hole=["As", "Kd"], community=["10h", "2c", "3d"], record=True, round_id=rid1)
    
    # 4. Round 1: Turn
    res3 = PokerService.analyze_hand(hole=["As", "Kd"], community=["10h", "2c", "3d", "4s"], record=True, round_id=rid1)
    
    # 5. Round 1: River
    res4 = PokerService.analyze_hand(hole=["As", "Kd"], community=["10h", "2c", "3d", "4s", "5d"], record=True, round_id=rid1)
    assert res4.hand_name == "Straight"
    
    # 6. Resolve Round 1
    HistoryService.resolve_round(rid1, outcome="win", net_chips=500)

    # --- GAME 2: LOSS (FOLD) ---
    # Reuse session sid
    # 7. Round 2: Pre-Flop
    res5 = PokerService.analyze_hand(hole=["7s", "8s"], record=True, session_id=sid)
    rid2 = res5.metadata["round_id"]
    assert rid2 != rid1
    
    # 8. Round 2: Flop (Bad board)
    res6 = PokerService.analyze_hand(hole=["7s", "8s"], community=["Ah", "Kh", "Qh"], record=True, round_id=rid2)
    
    # 9. Resolve Round 2 (Folded early)
    HistoryService.resolve_round(rid2, outcome="fold", net_chips=-50)

    # --- VERIFICATION ---
    with sqlite3.connect(test_env.db_path) as conn:
        # Check Session
        session = conn.execute("SELECT game_type, location FROM sessions WHERE session_id = ?", (sid,)).fetchone()
        assert session == ("poker", "Saint_Denis")
        
        # Check Rounds
        rounds = conn.execute("SELECT round_id, final_outcome, net_chips FROM rounds WHERE session_id = ? ORDER BY timestamp ASC", (sid,)).fetchall()
        assert len(rounds) == 2
        assert rounds[0][1] == "win"
        assert rounds[0][2] == 500
        assert rounds[1][1] == "fold"
        assert rounds[1][2] == -50
        
        # Check Snapshots
        snaps_r1 = conn.execute("SELECT count(*) FROM snapshots WHERE round_id = ?", (rid1,)).fetchone()[0]
        assert snaps_r1 == 4 # Pre-flop, Flop, Turn, River
        
        snaps_r2 = conn.execute("SELECT count(*) FROM snapshots WHERE round_id = ?", (rid2,)).fetchone()[0]
        assert snaps_r2 == 2 # Pre-flop, Flop
        
        # Verify JSON Blob content (UHH format)
        blob = conn.execute("SELECT game_state_json FROM snapshots WHERE round_id = ? LIMIT 1", (rid1,)).fetchone()[0]
        state = json.loads(blob)
        assert state["meta"]["game"] == "poker"
        assert "As" in state["state"]["hole"]
