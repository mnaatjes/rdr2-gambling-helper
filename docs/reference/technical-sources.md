---
title: Technical Sources & Decompiled Scripts
tags: [research, scripts, reverse-engineering, decompilation]
created-at: 2026-06-16
updated-at: 2026-06-16
---

# Technical Sources & Decompiled Scripts

This document provides quick-reference links to the primary technical resources used for understanding the underlying logic of RDR2 gambling systems.

## Script Repositories
These repositories contain C-like code translated from the game's compiled `.ysc` scripts.

*   **pyouneetm/RDR2-Decompiled-Scripts**
    *   **URL:** [https://github.com/pyouneetm/RDR2-Decompiled-Scripts](https://github.com/pyouneetm/RDR2-Decompiled-Scripts)
    *   **Git:** `https://github.com/pyouneetm/RDR2-Decompiled-Scripts.git`
    *   **Note:** High-quality source for cross-referencing mini-game logic. Look for `minigame_blackjack.c` and `minigame_poker.c`.

*   **kepmehz/RDR3-Decompiled-Scripts**
    *   **URL:** [https://github.com/kepmehz/RDR3-Decompiled-Scripts](https://github.com/kepmehz/RDR3-Decompiled-Scripts)
    *   **Note:** Comprehensive repository covering most game systems.

## Engine & Native Databases
Resources for understanding the engine-level functions (Natives) called by the scripts.

*   **RDR3 Native DB (alloc8or)**
    *   **URL:** [https://alloc8or.re/rdr3/nativedb/](https://alloc8or.re/rdr3/nativedb/)
    *   **Note:** Essential for looking up functions like `GET_RANDOM_INT_IN_RANGE` or UI-specific calls.
