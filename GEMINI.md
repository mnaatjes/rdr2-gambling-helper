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
- [x] Implement `--record` flag in `poker analyze` command.
- [x] Create `poker resolve` command to capture game outcomes.
- [ ] Document `dev report` requirements and calibration logic.

## Project Status
- **Phase 1: Infrastructure & Core Poker (COMPLETE)**
    - Standardized CLI with `rich` and `click`.
    - 7-Card Poker Evaluator.
    - Monte Carlo Equity Engine.
    - **Refactor:** Decoupled Service Layer with Pydantic V2 API (COMPLETE).
- **Phase 2: History & Calibration (IN PROGRESS)**
    - Integrated `HistoryService` for persistent hand recording.
    - Implemented `--record` and `resolve` in CLI.
    - **Next:** Define calibration logic for weight tuning.
