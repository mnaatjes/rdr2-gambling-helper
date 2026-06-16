# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-06-16

### Added
- Initial project scaffolding with MVC-inspired architecture.
- Modular Poker Engine with 7-card evaluator and Monte Carlo equity simulator.
- RDR2-specific Predictive Layer with NPC "Omniscience" weighting.
- High-fidelity `rich`-based CLI dashboard for poker analysis.
- **Service API Refactor**: Decoupled `PokerService` for programmatic usage.
- **History Service**: Multi-tier telemetry system (Sessions, Rounds, Snapshots) using SQLite.
- **CLI Context Manager**: Automatic session tracking with 12-character short IDs.
- Universal Hand History (UHH) JSON format for cross-game data persistence.
- Comprehensive documentation in Diataxis format.
- Integration test suite for full-game simulation.
