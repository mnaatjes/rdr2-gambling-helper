---
title: Frontend UI Branding & Design
tags: [design, branding, rdr2, ui, style-guide]
created-at: 2026-06-16
updated-at: 2026-06-16
---

# Frontend UI Branding & Design Document

## 1. Overview
The goal of the RDR2 Gambling Utility Web UI is to feel like a diegetic extension of the game world. The design mirrors the aesthetic of late 19th-century Americana, blending minimalist HUD elements with maximalist, parchment-based menus and ledgers.

## 2. Visual Identity & Palette

### Color Palette
We utilize high-contrast "Blood Red" accents against deep charcoal backgrounds, supported by "Parchment" neutrals for data-heavy views.

| Element | Hex Code | Description |
| :--- | :--- | :--- |
| **Primary Red** | `#EE0000` | Iconic RDR2 Red. Used for logos, active highlights, and critical alerts. |
| **Rich Black** | `#191C1F` | Main background for "HUD-style" dashboards. |
| **Parchment** | `#EFE1BD` | Background for "Ledger-style" history and settings views. |
| **Brass Gold** | `#7B612A` | Border accents, icon frames, and secondary highlights. |
| **Table Green** | `#1E4D2B` | Iconic RDR2 poker/blackjack felt green. Used for game-table display areas. |
| **Paper Ink** | `#2C2621` | Dark brown/black used for text on Parchment backgrounds. |
| **Pure White** | `#FFFFFF` | Primary text color on dark backgrounds. |

### Typography
To mirror the game's vintage hand-printed feel, we use web-equivalent fonts:

*   **Headings (Logo/Titles)**: **"Chinese Rocks"** (Web Alternative: *Rock Salt* or *Stencilia* for a rugged look).
*   **Subheadings/HUD**: **"Toronto Gothic"** (Web Alternative: *Bebas Neue* or *Oswald*).
*   **Body Text/Menus**: **"Clarendon"** or **"Kirsty"** (Web Alternative: *Sentinel* or *Roboto Slab*).
*   **Handwriting (Notes)**: **"Bandits"** (Web Alternative: *Homemade Apple* or *Cedarville Cursive*).

---

## 3. Page Structure

### Page 1: Game Selection (The "Saloon Entrance")
The landing page where the user chooses their assistance tool.
*   **Visuals**: Large, illustrative tiles with RDR2-style iconography.
*   **Options**:
    *   **Texas Hold'em**: Navigate to Poker Dashboard.
    *   **Blackjack**: Navigate to Blackjack Dashboard.
    *   **History**: Navigate to the Ledger.
    *   **Settings**: General configuration.

### Page 2: Game Dashboard (The "HUD View")
Every game page (Poker, Blackjack, etc.) follows a consistent **Two-Section Layout** optimized for the "Live Assistant" flow.

*   **Section A: The Interaction Forge (Input)**
    *   **Purpose**: Strategic data entry (cards, betting aggression, number of opponents).
    *   **Visuals**: Dark charcoal background with skeuomorphic buttons.
    *   **Layout**: High-density form layout designed for quick interaction.
*   **Section B: The Game Table (Display/Output)**
    *   **Purpose**: Real-time rendering of API results and hand visualizations.
    *   **Visuals**: Styled like a physical gambling table with **Table Green (`#1E4D2B`)** felt textures and brass border accents.
    *   **Features**: Displays the current "best hand" and win probabilities using the circular "HUD Core" equity gauges.

### Page 3: The History Ledger (The "Arthur's Journal" View)
A detailed review of past sessions using the Parchment theme.
*   **Visuals**: Two-column layout mimicking a 19th-century ledger or newspaper.
*   **Features**:
    *   Filterable list of sessions.
    *   Drill-down into specific rounds to see snapshots of "The Prediction" vs "The Outcome."
    *   Profit/Loss charts rendered in a hand-drawn style.

---

## 4. Component Styling Principles

*   **Universal Card Deck Components**
    *   We maintain a designated set of UI components for playing cards (`<GameCard />`).
    *   **Reusable**: The same component is utilized across Poker, Blackjack, and History views.
    *   **Dynamic**: Color-coded based on suit (`#EE0000` for Hearts/Diamonds, `#FFFFFF` for Spades/Clubs).
*   **Responsive & Mobile-Friendly**
    *   **Layout**: Uses CSS Grid and Flexbox to ensure the "Interaction Forge" and "Game Table" transition seamlessly from a side-by-side desktop view to a vertical mobile stack.
    *   **Inputs**: Touch-friendly card selectors designed for one-handed operation on mobile devices.
*   **Distressed Borders**: Use CSS masks or SVG filters to give panels a slightly "torn paper" or "weathered wood" edge.
*   **The "Cores" Style**: Use circular progress bars for win equity that mirror the Health/Stamina "Cores" from the game's HUD.
*   **Skeuomorphic Inputs**: Buttons should look like stamped metal or carved wood, rather than flat digital rectangles.
*   **Red Ink Bleeds**: Alerts and errors should use the Primary Red with a subtle blur to simulate ink soaking into paper.

---

## 5. User Flows

### "The Live Assistant" Flow
1.  **Selection**: User clicks "Poker" from the Saloon page.
2.  **Input**: User taps icons in the "Interaction Forge" to select their cards. Visual feedback shows the selected cards in a "fan" layout.
3.  **Simulation**: API call is triggered. A loading state shows a subtle "spinning revolver cylinder" animation.
4.  **Advice**: The "Game Table" section updates with the recommendation and equity "Cores."
5.  **Log**: User taps a "Save Snapshot" icon to record to the History Service.

### "The Post-Game Review" Flow
1.  **Navigation**: User selects "History" from the main menu.
2.  **Browse**: User scrolls through the Ledger (Parchment theme).
3.  **Insight**: User expands a round to see a timeline of how their win probability changed from Flop to River.
