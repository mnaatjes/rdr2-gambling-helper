---
title: How to Use the Poker Service API
tags: [api, poker, integration, python]
created-at: 2026-06-16
updated-at: 2026-06-16
---

# How to Use the Poker Service API

This guide explains how to programmatically interact with the `PokerService` to analyze hands and record history. This service is designed to be used as a standalone Python library by other services or automation scripts.

## 1. Importing the Service

To use the service, import the `PokerService` class and the necessary models:

```python
from core.poker.service import PokerService
from core.poker.models import Card
```

## 2. Analyzing a Hand (Basic)

The `analyze_hand` method is the primary entry point. It handles parsing, simulation, and recommendation.

### Standard Request
```python
result = PokerService.analyze_hand(
    hole=["As", "Kd"],          # Shorthand strings or Card objects
    community=["10h", "2c"],    # Optional community cards
    num_opponents=3,            # Number of NPCs
    iterations=2000             # Accuracy of Monte Carlo simulation
)

print(f"Hand: {result.hand_name}")
print(f"Win Rate: {result.win_rate:.2%}")
print(f"Recommendation: {result.recommendation}")
```

## 3. Telemetry & History Recording

The API allows you to record snapshots to the unified History database by setting the `record` flag.

### Recording with Automatic Session/Round Management
If you only provide `record=True`, the service will automatically handle session creation or use an existing round if possible.

```python
result = PokerService.analyze_hand(
    hole=["As", "Kd"],
    record=True
)
# Access the generated round ID
round_id = result.metadata["round_id"]
```

### Explicit Round Tracking (Recommended)
For multi-street analysis (Flop, Turn, River), you should pass the `round_id` explicitly to link snapshots together.

```python
# 1. Analyze Flop
flop_res = PokerService.analyze_hand(hole=["As", "Ks"], community=["10s", "2h", "3d"], record=True)
rid = flop_res.metadata["round_id"]

# 2. Analyze Turn (using the same round_id)
turn_res = PokerService.analyze_hand(hole=["As", "Ks"], community=["10s", "2h", "3d", "Js"], record=True, round_id=rid)
```

## 4. Input Parameters Reference

| Parameter | Type | Default | Description |
| :--- | :--- | :--- | :--- |
| `hole` | `List[str]` \| `List[Card]` | **Required** | Two cards representing the player's hand. |
| `community` | `List[str]` \| `List[Card]` | `[]` | Up to 5 community cards. |
| `num_opponents` | `int` | `1` | Number of NPCs at the table. |
| `aggression` | `List[float]` | `[0.2]*N` | List of 0.0-1.0 values for NPC intensity. |
| `iterations` | `int` | `2000` | Simulation depth. Higher = slower/more accurate. |
| `record` | `bool` | `False` | Whether to save the snapshot to the database. |
| `round_id` | `str` | `None` | Existing Round ID to associate the snapshot with. |
| `session_id` | `str` | `None` | Session ID to use if starting a new round. |

## 5. What to Expect Back (`SimulationResult`)

The service returns a `SimulationResult` Pydantic model. You can convert this to a dictionary using `.model_dump()`.

### Response Schema
*   `win_rate` (float): Probability of winning (0.0 to 1.0).
*   `tie_rate` (float): Probability of a split pot.
*   `loss_rate` (float): Probability of losing.
*   `hand_name` (str): Semantic name of current best hand (e.g., "Full House").
*   `recommendation` (str): Rich-formatted string with actionable advice.
*   `equity_iterations` (int): Number of sims performed.
*   `metadata` (dict): Contains `round_id` if recorded.

## 6. Error Handling
The service raises standard Python exceptions if inputs are invalid:
*   `ValueError`: If card strings are malformed (e.g., "Zx").
*   `KeyError`: If required parameters are missing in the data models.
