import pytest
import os
import sqlite3
from pathlib import Path
from core.history.service import HistoryService
from core.history.db import HistoryDB

@pytest.fixture
def temp_db(tmp_path):
    db_path = tmp_path / "test_history.db"
    # Monkeypatch the DB path in HistoryService
    original_db = HistoryService._db
    HistoryService._db = HistoryDB(db_path=db_path)
    yield HistoryService._db
    HistoryService._db = original_db

def test_history_workflow(temp_db):
    # 1. Start Session
    sid = HistoryService.start_session(game_type="poker", location="Valentine")
    assert len(sid) == 12
    
    # 2. Start Round (Explicitly pass sid)
    rid = HistoryService.start_round(session_id=sid)
    assert len(rid) == 12
    
    # 3. Record Snapshot
    state = {"cards": ["As", "Kd"]}
    pred = {"win_rate": 0.5}
    snid = HistoryService.record_snapshot(rid, state, pred)
    assert len(snid) == 12
    
    # 4. Resolve Round
    HistoryService.resolve_round(rid, outcome="win", net_chips=100)

def test_cli_context(tmp_path):
    from cli.context import CLIContext, CONTEXT_FILE
    import os
    
    # Mock CONTEXT_FILE path
    original_path = CONTEXT_FILE
    new_path = tmp_path / "test_context.json"
    import cli.context
    cli.context.CONTEXT_FILE = new_path
    
    try:
        # Test Set/Get
        CLIContext.set_active_session("poker", "abc123456789")
        assert CLIContext.get_active_session("poker") == "abc123456789"
        
        # Test Clear
        CLIContext.clear_session("poker")
        assert CLIContext.get_active_session("poker") is None
    finally:
        cli.context.CONTEXT_FILE = original_path
