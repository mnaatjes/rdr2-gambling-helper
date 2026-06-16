# Red Dead Redemtion 2: Gambling Utility

## Directives

- Always verify with user before implementing changes
- Never delete/edit content or code without prior approval
- Teach the user about what actions you are taking
- Recommend to user well-researched options upon request
- Provide concise and bullet-point information
- Test everything using pytest as being built and before implementation
- Track project status in GEMINI.md (this document) sub-section
- Track TODOs in GEMINI.md (this document) sub-section


## Architecture
- Documentation in docs/ follows diataxis format
- All markdown documentation must include frontmatter properties: title, tags, created-at, updated-at
- Coding abd tooling in python
- Testing done using pytest

## TODOs
- [ ] Initialize `src/core/telemetry/db.py` with SQLite schema.
- [ ] Implement `--record` flag in `poker analyze` command.
- [ ] Create `poker resolve` command to capture game outcomes.
- [ ] Implement `dev report` for precision analysis and weight calibration.

## Project Status
- **Phase 1: Infrastructure & Core Poker (COMPLETE)**
    - Standardized CLI with `rich` and `click`.
    - 7-Card Poker Evaluator.
    - Monte Carlo Equity Engine.
    - **Refactor:** Decoupled Service Layer with Pydantic V2 API (COMPLETE).
- **Phase 2: Telemetry & Calibration (IN PROGRESS)**
    - Architecture ready for telemetry integration via `PokerService`.
    - Planning SQLite schema for hand recording.
