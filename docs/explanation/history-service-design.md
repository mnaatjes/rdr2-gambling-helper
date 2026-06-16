---
title: History Service Design
tags: [architecture, telemetry, database, history, poker, blackjack]
created-at: 2026-06-16
updated-at: 2026-06-16
---

# History Service Design Document

## 1. Overview
The **History Service** (Service B) acts as a centralized "Silent Recorder" for all RDR2 gambling activities. Its primary goal is to persist every decision, recommendation, and outcome into a structured "Data Lake" without interfering with the live game logic (Service A).

## 2. Multi-Tier Relational Schema
The service utilizes a three-tier hierarchy to allow scaling from individual hand snapshots to broad session-based analysis.

### Tier 1: `sessions` (Context)
Captures the "When" and "Where" of a gambling session.
*   `session_id` (UUID/Primary Key)
*   `game_type` (TEXT: 'poker', 'blackjack')
*   `location` (TEXT: 'Valentine', 'Saint_Denis', etc.)
*   `start_time` (TIMESTAMP)

### Tier 2: `rounds` (Outcome)
Captures the "Result" of a specific game round (e.g., a single Poker hand or Blackjack deal).
*   `round_id` (UUID/Primary Key)
*   `session_id` (FK -> sessions.session_id)
*   `timestamp` (TIMESTAMP)
*   `final_outcome` (TEXT: 'win', 'loss', 'tie', 'fold', 'null')
*   `net_chips` (INTEGER: Optional profit/loss tracking)

### Tier 3: `snapshots` (Logic Trace)
Captures the "Thinking" of the tool at any specific moment during a round.
*   `snapshot_id` (UUID/Primary Key)
*   `round_id` (FK -> rounds.round_id)
*   `game_state_json` (TEXT/JSON: The raw state from Service A)
*   `prediction_json` (TEXT/JSON: The full SimulationResult from Service A)

---

## 3. Universal Data Representation (UHH Format)
To ensure the History Service can handle any game without schema changes, we utilize a **Universal Hand History (UHH)** format for the JSON blobs.

### Game State Blob (`game_state_json`)
All game services (Poker, Blackjack, etc.) must provide a state object following this structure:
```json
{
  "meta": {
    "version": "1.0",
    "game": "poker"
  },
  "state": {
    "hole": ["As", "Kd"],
    "community": ["10h"],
    "opponents": 2,
    "context": {
      "aggression": [0.8, 0.2],
      "pot_size": 150
    }
  }
}
```

### Prediction Blob (`prediction_json`)
Direct serialization of the `SimulationResult` Pydantic model:
```json
{
  "win_rate": 0.43,
  "hand_name": "Incomplete Hand",
  "recommendation": "CALL / VALUE BET",
  "metadata": {
    "iterations": 2000,
    "engine": "RDR2Predictive"
  }
}
```

---

## 4. Implementation Roadmap

### Phase 1: Storage Engine
*   Initialize `src/core/history/db.py` with SQLite/Aiosqlite.
*   Implement the `HistoryService` class with `start_session`, `record_snapshot`, and `resolve_round` methods.

### Phase 2: Service A Integration (Poker)
*   Modify `PokerService.analyze_hand` to optionally accept a `round_id`.
*   If provided, the service will automatically trigger a `record_snapshot` call.

### Phase 3: CLI Integration
*   Add the `--record` flag to `rdr2-gambler poker analyze`.
*   Implement the `rdr2-gambler poker resolve` command to update the `final_outcome`.

## 5. Future Capability: Calibration
Once the Data Lake is populated, a separate `CalibrationService` will query the `snapshots` and `rounds` tables to calculate the **"Delta"** between predicted win rates and actual outcomes, allowing for automated tuning of NPC aggression weights.
