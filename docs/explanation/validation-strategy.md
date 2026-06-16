---
title: Validation & Telemetry Strategy
tags: [validation, telemetry, sqlite, calibration, research]
created-at: 2026-06-16
updated-at: 2026-06-16
---

# Validation & Telemetry Strategy

This document outlines the approach for verifying the accuracy of the `rdr2-gambler` utility and the strategy for calibrating its predictive logic against real-world game data.

## 1. Validation Strategy & Simulation Analysis

The primary challenge in validating this tool is verifying the **RDR2-specific predictive layer** rather than the standard poker math.

### Mathematical Accuracy (Standard Logic)
The core Hand Evaluator and Monte Carlo engine are verified using "Golden Sets" of known poker hands and pre-calculated odds. 
*   **Verdict:** Current unit tests in `tests/test_poker.py` are sufficient for standard accuracy.

### RDR2 Prediction Accuracy (Exploitative Logic)
The "X-Factor" is our tool's ability to anticipate RDR2's "Omniscient" NPCs.
*   **The Risk:** Over-weighting NPC aggression might lead to false "Fold" recommendations.
*   **The Need:** A mechanism to calibrate our weights against actual game outcomes.

### The "Scenario Runner" Approach
Instead of a full-scale game simulator, we utilize a **Scenario Runner** (`tests/test_rdr2_scenarios.py`) to compare tool advice against documented RDR2 "Bad Beat" scenarios sourced from community research.

## 2. Telemetry & Calibration (Data-Driven Feedback)

To achieve high fidelity, we implement a persistent telemetry system using SQLite to track tool performance during actual play sessions.

### Database Schema (`core/telemetry/db.py`)
The lightweight database tracks the following for every recorded hand:
*   `hand_id`: Unique session identifier.
*   `timestamp`: When the hand was recorded.
*   `state`: Current game stage (Hole, Flop, Turn, River).
*   `prediction_win_rate`: The win probability calculated by the tool.
*   `prediction_recommendation`: The specific move recommended (Fold, Call, Raise).
*   `actual_outcome`: Final result (Win, Loss, Tie).
*   `npc_behavior`: Observed NPC aggression level.
*   `location`: World location (e.g., Saint Denis, Valentine) to track regional variance.

## 3. Architecture & Implementation

### Package Structure
The telemetry logic is decoupled from the core utility to minimize overhead:
```text
src/
├── cli/
│   └── cmd_dev.py       # Admin/Dev CLI commands
└── core/
    └── telemetry/
        ├── __init__.py
        └── db.py        # SQLite connection and schema logic
```

### CLI Entry Points
*   **Capture Mode**: Users can record hands during analysis.
    ```bash
    rdr2-gambler poker analyze --hole As Kd --record
    ```
*   **Resolution**: Users close the loop by reporting the final outcome.
    ```bash
    rdr2-gambler poker resolve --id <hand_id> --winner NPC
    ```
*   **Calibration Report**: A dev-specific command to analyze precision.
    ```bash
    rdr2-gambler dev report --precision
    ```

### UI Design (Dev Reporting)
The `dev report` utilizes a stylized `Rich` dashboard to present:
*   **Confidence Interval**: How often the "Actual Outcome" matched our "Recommended Action."
*   **Variance Analysis**: Identifying if the tool is consistently too optimistic or too cautious.
*   **Calibration Advice**: Automatic suggestions for adjusting the `predictive.py` weights (e.g., "Increase NPC Omniscience factor by 10%").
