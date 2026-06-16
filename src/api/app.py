from flask import Flask, request, jsonify
from flask_cors import CORS
from core.poker.service import PokerService
from core.history.service import HistoryService
from pydantic import ValidationError

app = Flask(__name__)
CORS(app) # Enable CORS for all routes

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "healthy", "service": "rdr2-gambler-api"})

@app.route('/api/poker/analyze', methods=['POST'])
def poker_analyze():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        # Extract parameters from request
        hole = data.get('hole')
        community = data.get('community', [])
        opponents = data.get('opponents', 1)
        aggression = data.get('aggression')
        record = data.get('record', False)
        round_id = data.get('round_id')
        session_id = data.get('session_id')

        # Call the existing PokerService
        result = PokerService.analyze_hand(
            hole=hole,
            community=community,
            num_opponents=opponents,
            aggression=aggression,
            record=record,
            round_id=round_id,
            session_id=session_id
        )

        return jsonify(result.model_dump())

    except ValidationError as e:
        return jsonify({"error": "Validation Error", "details": e.errors()}), 422
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/history/sessions', methods=['GET'])
def get_sessions():
    db = HistoryService.get_db()
    with db._get_connection() as conn:
        sessions = conn.execute(
            "SELECT session_id, game_type, location, start_time FROM sessions ORDER BY start_time DESC LIMIT 10"
        ).fetchall()
    
    return jsonify([
        {"id": s[0], "game": s[1], "location": s[2], "started": s[3]} for s in sessions
    ])

@app.route('/api/history/rounds', methods=['GET'])
def get_rounds():
    session_id = request.args.get('session_id')
    db = HistoryService.get_db()
    query = "SELECT round_id, session_id, timestamp, final_outcome, net_chips FROM rounds"
    params = []
    
    if session_id:
        query += " WHERE session_id = ?"
        params.append(session_id)
    
    query += " ORDER BY timestamp DESC LIMIT 20"
    
    with db._get_connection() as conn:
        rounds = conn.execute(query, tuple(params)).fetchall()
        
    return jsonify([
        {"id": r[0], "session_id": r[1], "timestamp": r[2], "outcome": r[3], "chips": r[4]} for r in rounds
    ])

@app.route('/api/history/resolve', methods=['POST'])
def resolve_round():
    data = request.get_json()
    round_id = data.get('id')
    outcome = data.get('outcome')
    chips = data.get('chips')
    
    if not round_id or not outcome:
        return jsonify({"error": "Missing round_id or outcome"}), 400
        
    try:
        HistoryService.resolve_round(round_id, outcome, chips)
        return jsonify({"status": "success", "round_id": round_id})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
