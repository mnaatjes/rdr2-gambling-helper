import sqlite3
import json
import uuid
from datetime import datetime
from typing import Optional, Dict, List
from pathlib import Path

DEFAULT_DB_PATH = Path.home() / ".rdr2-gambler" / "history.db"

class HistoryDB:
    def __init__(self, db_path: Optional[Path] = None):
        self.db_path = db_path or DEFAULT_DB_PATH
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_db()

    def _get_connection(self):
        return sqlite3.connect(self.db_path)

    def _init_db(self):
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS sessions (
                    session_id TEXT PRIMARY KEY,
                    game_type TEXT NOT NULL,
                    location TEXT,
                    start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS rounds (
                    round_id TEXT PRIMARY KEY,
                    session_id TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    final_outcome TEXT,
                    net_chips INTEGER,
                    FOREIGN KEY (session_id) REFERENCES sessions (session_id)
                )
            """)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS snapshots (
                    snapshot_id TEXT PRIMARY KEY,
                    round_id TEXT,
                    game_state_json TEXT,
                    prediction_json TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (round_id) REFERENCES rounds (round_id)
                )
            """)
            conn.commit()

    def _generate_id(self) -> str:
        return uuid.uuid4().hex[:12]

    def create_session(self, game_type: str, location: Optional[str] = None) -> str:
        session_id = self._generate_id()
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO sessions (session_id, game_type, location) VALUES (?, ?, ?)",
                (session_id, game_type, location)
            )
        return session_id

    def create_round(self, session_id: str) -> str:
        round_id = self._generate_id()
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO rounds (round_id, session_id) VALUES (?, ?)",
                (round_id, session_id)
            )
        return round_id

    def add_snapshot(self, round_id: str, state_json: str, prediction_json: str) -> str:
        snapshot_id = self._generate_id()
        with self._get_connection() as conn:
            conn.execute(
                "INSERT INTO snapshots (snapshot_id, round_id, game_state_json, prediction_json) VALUES (?, ?, ?, ?)",
                (snapshot_id, round_id, state_json, prediction_json)
            )
        return snapshot_id

    def resolve_round(self, round_id: str, outcome: str, net_chips: Optional[int] = None):
        with self._get_connection() as conn:
            conn.execute(
                "UPDATE rounds SET final_outcome = ?, net_chips = ? WHERE round_id = ?",
                (outcome, net_chips, round_id)
            )

    def get_last_session_id(self, game_type: str) -> Optional[str]:
        with self._get_connection() as conn:
            res = conn.execute(
                "SELECT session_id FROM sessions WHERE game_type = ? ORDER BY start_time DESC LIMIT 1",
                (game_type,)
            ).fetchone()
            return res[0] if res else None

    def get_last_round_id(self, session_id: str) -> Optional[str]:
        with self._get_connection() as conn:
            res = conn.execute(
                "SELECT round_id FROM rounds WHERE session_id = ? ORDER BY timestamp DESC LIMIT 1",
                (session_id,)
            ).fetchone()
            return res[0] if res else None
