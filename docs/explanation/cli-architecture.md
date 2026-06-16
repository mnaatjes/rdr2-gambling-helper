---
title: CLI Architecture
tags: [architecture, cli, design, explanation]
created-at: 2026-06-16
updated-at: 2026-06-16
---

# CLI Architecture

This document outlines the structural design and operational philosophy of the `rdr2-gambler` command-line interface.

## 1. Command Anatomy

The executable follows a hierarchical structure to provide a clear interface for different mini-games and actions.

```bash
rdr2-gambler [GLOBAL_OPTIONS] <game> [GAME_OPTIONS] [ARGS]
```

### Subcommands
*   **Games:** `blackjack`, `poker`, `dominoes`, `five-finger`.
*   **Actions:** Specific operations within a game context.
    *   Example: `rdr2-gambler poker simulate`
    *   Example: `rdr2-gambler blackjack odds`

## 2. Standard Conventions

To ensure a predictable user experience, the CLI adheres to POSIX/GNU flag conventions.

### Short & Long Flags
*   `-h, --help`: Context-sensitive help. Typing `rdr2-gambler <game> --help` provides game-specific usage.
*   `-v, --verbose`: Enables debug logging, directed to `stderr`.
*   `-q, --quiet`: Suppresses non-essential output, ensuring `stdout` contains only raw data (CSV/JSON).
*   `-V, --version`: Displays the current version of the utility.

### Input Separation
The double dash (`--`) is used to signal the end of options. Anything following it is treated as an argument, protecting against inputs that start with a dash.

## 3. I/O & UI Strategy

### Standard Streams
*   **`stdout`**: Reserved for primary data output, such as hand probabilities, recommended moves, or simulation results. This allows for easy piping into other tools.
*   **`stderr`**: Used for metadata, progress bars (via `Rich`), table borders, diagnostics, and "House" advice.

### Exit Codes
*   `0`: Success. Calculation complete or move successfully identified.
*   `1`: Logic error (e.g., inputting an impossible card combination).
*   `2`: CLI usage error (e.g., providing invalid flags or missing arguments).

## 4. Execution Flow

The CLI follows a robust lifecycle to ensure stability and flexibility:

1.  **Config Load**: Attempt to load default "House" rules and user preferences from `~/.config/rdr2_gambler/rules.json`.
2.  **Arg Parsing**: Utilize the `click` library to manage subcommand nesting and automatic help generation.
3.  **TTY Detection**:
    *   **Interactive**: Render high-fidelity card displays using `Rich` panels and colors.
    *   **Piped**: Automatically strip styling and output raw text or JSON for machine readability.
4.  **Signal Trap**: Implement a graceful shutdown for `KeyboardInterrupt` (Ctrl+C) to prevent stack traces during long simulations.

## 5. Package Structure

The project implements an **MVC-Inspired** architecture to separate concerns between routing, UI, and game logic:

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
