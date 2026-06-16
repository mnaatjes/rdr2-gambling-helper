import json
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

CONTEXT_FILE = Path.home() / ".rdr2-gambler" / "context.json"
SESSION_TIMEOUT_HOURS = 4

class CLIContext:
    @staticmethod
    def _load() -> Dict[str, Any]:
        if not CONTEXT_FILE.exists():
            return {}
        try:
            with open(CONTEXT_FILE, "r") as f:
                return json.load(f)
        except:
            return {}

    @staticmethod
    def _save(data: Dict[str, Any]):
        CONTEXT_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(CONTEXT_FILE, "w") as f:
            json.dump(data, f, indent=2)

    @classmethod
    def get_active_session(cls, game_type: str) -> Optional[str]:
        data = cls._load()
        session = data.get(game_type)
        if not session:
            return None
        
        # Check for timeout
        start_time = datetime.fromisoformat(session["start_time"])
        if datetime.now() - start_time > timedelta(hours=SESSION_TIMEOUT_HOURS):
            return None
            
        return session["session_id"]

    @classmethod
    def set_active_session(cls, game_type: str, session_id: str):
        data = cls._load()
        data[game_type] = {
            "session_id": session_id,
            "start_time": datetime.now().isoformat()
        }
        cls._save(data)

    @classmethod
    def clear_session(cls, game_type: str):
        data = cls._load()
        if game_type in data:
            del data[game_type]
            cls._save(data)
