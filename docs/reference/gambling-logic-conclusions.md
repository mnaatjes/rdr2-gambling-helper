---
title: Gambling Logic Conclusions
tags: [logic, blackjack, poker, architecture, ai]
created-at: 2026-06-16
updated-at: 2026-06-16
---

# Gambling Logic Conclusions

Technical summary of the architectural and behavioral patterns identified within Rockstar's gambling implementations.

## Technical Logic Overviews

### Finite State Machine (FSM)
Rockstar utilizes a rigid FSM architecture for all gambling mini-games. This ensures the game cycles through deterministic states to maintain flow without logic errors:
*   `STATE_BETTING`
*   `STATE_DEALING`
*   `STATE_PLAYER_TURN`

### Blackjack Dealer AI
The dealer's logic is strictly procedural and follows standard house rules without complex decision-making:
*   **Dealer Hit:** If total is `< 17`
*   **Dealer Stand:** If total is `>= 17`

### Poker NPC Archetypes
NPCs are assigned specific "personalities" that dictate their betting thresholds. Decisions are weighted based on "Hand Strength" vs. "Pot Odds":
*   **Aggressive:** Frequent raises, higher risk tolerance.
*   **Passive:** Prefers checking and calling.
*   **Bluffer:** Likely to bet high on low-strength hands to force folds.

## Key Findings for Implementation

### Random Number Generation (RNG)
The game uses standard engine-level `GET_RANDOM_INT_IN_RANGE` calls for shuffling and dealing. 
*   **Fairness:** There is no evidence of the deck being "rigged" for player losses in general play.
*   **Scripted Events:** Certain story-related hands are hard-coded for narrative purposes.

### Scaleform UI
Interactive menus and betting prompts are handled via the **Scaleform** (Flash-based) system. The main script thread sends data packets to the UI component to update displays in real-time.

### Scripted Props
Cards and chips are handled as scripted props rather than complex physics objects.
*   **Textures:** Dynamic textures are assigned to card props based on the integer value drawn from the virtual deck array.
