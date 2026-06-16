# Red Dead Redemption 2 Gambling Utility

![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)

## Description

This is a utility that has scripts to aid in gambling help

- Follows the rules of a specific game
- Researched specifics and particularities of RDR2 Gambling Implementations

## Project Structure

```text
src/
├── __init__.py
├── __main__.py          # Entry point
├── cli/                 # (Controller) Click command routing
│   ├── __init__.py
│   ├── main.py          # Global options & group definition
│   ├── cmd_blackjack.py # 'rdr2-gambler blackjack' routing
│   └── cmd_poker.py
├── ui/                  # (View) Rich rendering logic
│   ├── __init__.py
│   ├── renderers.py     # Functions that return Rich Tables/Panels
│   └── themes.py        # Color palettes
└── core/                # (Model) Pure Game Logic
    ├── __init__.py
    └── poker/           # Modular poker logic
        ├── evaluator.py
        ├── engine.py
        ├── models.py
        └── predictive.py
```
