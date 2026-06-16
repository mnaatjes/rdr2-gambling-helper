# Project Status: RDR2 Gambling Utility

## Current Version: 0.1.0 (Scaffold & Poker Alpha)

### Phase 1: Infrastructure & Core Poker (COMPLETE)
- [x] Project scaffolding with MVC-inspired architecture.
- [x] Standardized CLI with `click` and `rich`.
- [x] Flat `src/` layout with `pyproject.toml` entry point.
- [x] 7-Card Poker Evaluator (High Card to Straight Flush).
- [x] Monte Carlo Probability Engine (Equity calculation).
- [x] RDR2-specific Predictive Layer (NPC Aggression Weighting).
- [x] High-fidelity Rich UI Dashboard for Poker.
- [x] Comprehensive Documentation (Diataxis-compliant).

### Phase 2: Telemetry & Calibration (IN PROGRESS)
- [ ] Initialize `src/core/telemetry/db.py` with SQLite schema.
- [ ] Implement `--record` flag in `poker analyze` command.
- [ ] Create `poker resolve` command to capture game outcomes.
- [ ] Implement `dev report` for precision analysis and weight calibration.
- [ ] Scenario-based testing in `tests/test_rdr2_scenarios.py`.

### Phase 3: Blackjack & Other Games (PLANNED)
- [ ] Implement Blackjack Dealer FSM (Hit on < 17).
- [ ] Blackjack Odds Engine (Dealer bust probability).
- [ ] Dominoes logic (Tile counting and placement strategy).
- [ ] Five Finger Fillet (Pattern sequence trainer).

---

## Active TODOs
1. **Telemetry Base:** Set up the SQLite database connection logic in `src/core/telemetry/`.
2. **Data Capture:** Modify `src/cli/cmd_poker.py` to support the `--record` flag.
3. **Resolution Logic:** Create the CLI command to update hand records with final outcomes.
4. **Validation:** Source RDR2 "Bad Beat" data for initial calibration scenarios.
