---
title: RDR2 Branding & Style Reference
tags: [reference, design, branding, fonts, colors]
created-at: 2026-06-16
updated-at: 2026-06-16
---

# Red Dead Redemption 2 Branding & Style Reference

This document serves as a technical reference for the visual identity of Red Dead Redemption 2 (RDR2). It is intended to guide the frontend development of the Gambling Utility to ensure aesthetic consistency with the game world.

## 1. Typography Standards

### Core Branding Font
The primary font used for the Red Dead Redemption logo, box art, and major marketing materials:
*   **Chinese Rocks** (specifically **Chinese Rocks Rg**): A rugged, stencil-style font designed by Ray Larabie. It features distressed edges and uneven strokes that evoke a hand-stamped look.
*   **Web Alternative**: *Rock Salt* or *Stencilia* (for ruggedness) or *Bebas Neue* (for HUD cleanliness).

### Map Typography (Diegetic Reference)
The following fonts are used within the in-game world map to distinguish various landmarks and features:

| Feature Type | Font Name (Close Match) | Note |
| :--- | :--- | :--- |
| **Major Water Body** | Garamond Italic | Large rivers and oceans. |
| **Minor Lakes** | Fabrizio Inferior | Smaller interior bodies of water. |
| **City/Station/Forts** | Gordon Black | High-visibility urban markers. |
| **State Name** | Foundry Origin | Wide, blocky tracking for regions. |
| **Natural Feature** | Boronia | Mountains, valleys, and forests. |
| **Viewpoint** | Larissa Handwriting | Personal points of interest/notes. |

### UI & HUD Typography
*   **HUD Readability**: Clean, condensed sans-serifs (similar to *Chalet London 1960* or *Toronto Gothic*).
*   **Journal/Handwriting**: Distressed cursive scripts mimicking Arthur Morgan's personal notes (e.g., *Homemade Apple*).

---

## 2. Color Palette (Hex Codes)

The RDR2 palette is grounded in a "maximalist" high-contrast scheme of red and black, supported by organic, weathered neutrals.

### Primary Brand Colors
| Element | Hex Code | Visual Preview | Description |
| :--- | :--- | :--- | :--- |
| **Iconic Red** | `#EE0000` | ![#EE0000](https://via.placeholder.com/15/EE0000?text=+) | The standard "Red Dead" red used in the logo. |
| **Blood Red** | `#B90303` | ![#B90303](https://via.placeholder.com/15/B90303?text=+) | Used for deeper UI accents and "ink bleed" effects. |
| **Deep Crimson** | `#BD081A` | ![#BD081A](https://via.placeholder.com/15/BD081A?text=+) | High-contrast variant for menu highlights. |

### Environmental & HUD Colors
| Element | Hex Code | Visual Preview | Description |
| :--- | :--- | :--- | :--- |
| **Rich Black** | `#121212` | ![#121212](https://via.placeholder.com/15/121212?text=+) | Primary background for HUD and dark menus. |
| **Table Green** | `#1E4D2B` | ![#1E4D2B](https://via.placeholder.com/15/1E4D2B?text=+) | Felt texture color used for Poker and Blackjack tables. |
| **Parchment** | `#EFE1BD` | ![#EFE1BD](https://via.placeholder.com/15/EFE1BD?text=+) | "Satin Souffle" neutral used for journals and ledgers. |
| **Brass Gold** | `#7B612A` | ![#7B612A](https://via.placeholder.com/15/7B612A?text=+) | "Brazen Brass" for borders, icon rings, and status highlights. |
| **Sunburst** | `#FEAC01` | ![#FEAC01](https://via.placeholder.com/15/FEAC01?text=+) | Golden-yellow used for fortified cores and active mission markers. |

---

## 3. Visual Language & HUD Design

### The "Core" System
The most iconic element of the RDR2 interface.
*   **Circular Layout**: A central icon (Heart, Lightning, Eye) encased in a ring.
*   **Status Indicators**: The inner icon represents long-term "Core" health, while the outer ring represents immediate resource depletion.
*   **Application**: Use this pattern for win-rate "gauges" in the Poker Dashboard.

### Diegetic Philosophy
*   **Weathered Textures**: UI panels should not be "clean." They should feature subtle ink bleeds, distressed edges (paper/wood), and stamp-like imperfections.
*   **Minimalist HUD**: During active play (Game Dashboards), the UI should be pushed to the edges of the frame to maintain a "cinematic" feel.
*   **Rule of Thirds**: Group functional clusters (Inputs vs. Display) into distinct corner-weighted regions.

## 4. UI Component Design Principles
1.  **Skeuomorphism**: Buttons should look like stamped metal, leather tabs, or carved wood.
2.  **Translucency**: HUD backgrounds should use a 60-80% opacity variant of `Rich Black` (`#121212`) to allow the game world (or background images) to bleed through.
3.  **Border Integrity**: Use thin, sharp brass borders for modern HUD elements and distressed/torn edges for history/journal views.
