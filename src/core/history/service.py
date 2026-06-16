from typing import Optional, Dict, Any
from .db import HistoryDB
import json

class HistoryService:
    _db: Optional[HistoryDB] = None

    @classmethod
    def get_db(cls) -> HistoryDB:
        if cls._db is None:
            cls._db = HistoryDB()
        return cls._db

    @classmethod
    def start_session(cls, game_type: str, location: Optional[str] = None) -> str:
        return cls.get_db().create_session(game_type, location)

    @classmethod
    def start_round(cls, session_id: str) -> str:
        """Starts a new round. Explicitly requires a session_id."""
        return cls.get_db().create_round(session_id)

    @classmethod
    def record_snapshot(cls, round_id: str, state: Dict[str, Any], prediction: Dict[str, Any]) -> str:
        return cls.get_db().add_snapshot(
            round_id,
            json.dumps(state),
            json.dumps(prediction)
        )

    @classmethod
    def resolve_round(cls, round_id: str, outcome: str, net_chips: Optional[int] = None):
        cls.get_db().resolve_round(round_id, outcome, net_chips)

    @classmethod
    def get_active_round(cls, game_type: str) -> Optional[str]:
        db = cls.get_db()
        session_id = db.get_last_session_id(game_type)
        if session_id:
            return db.get_last_round_id(session_id)
        return None
