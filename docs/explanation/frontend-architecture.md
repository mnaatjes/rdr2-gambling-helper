---
title: Frontend Vue.js Architecture
tags: [architecture, vue, vite, sass, pinia, vitest]
created-at: 2026-06-16
updated-at: 2026-06-16
---

# Frontend Vue.js Architecture

## 1. Overview
The RDR2 Gambling Utility Frontend is a modern, reactive web application built with **Vue.js 3**. It serves as a visual alternative to the CLI, providing high-fidelity dashboards and interactive controls for gambling analysis.

## 2. Tech Stack & Tooling
*   **Framework**: Vue.js 3 (Composition API)
*   **Build Tool**: Vite (Next-generation frontend tooling)
*   **State Management**: Pinia (Intuitive, type-safe store)
*   **Styling**: SASS/SCSS (Modular, pre-processed CSS)
*   **API Client**: Axios (Promise-based HTTP client)
*   **Testing**: Vitest + Vue Test Utils (Fast unit/component testing)
*   **Routing**: Vue Router (SPA navigation)

---

## 3. Directory Structure
```text
web/
├── src/
│   ├── assets/         # Global SASS (variables, mixins, reset)
│   ├── components/     # Atomic UI components
│   │   ├── atomic/     # Smallest units (Cards, Buttons, Inputs)
│   │   └── molecules/  # Compound units (Form Groups, Hand Displays)
│   ├── views/          # Page-level components
│   ├── store/          # Pinia modules (session.js, poker.js)
│   ├── services/       # API abstraction (api.js)
│   ├── router/         # Navigation config
│   └── App.vue         # Root Layout
├── tests/              # Vitest test suites
├── package.json
└── vite.config.js      # Build & SASS configuration
```

---

## 4. Component & View Roadmap

### Core Components
*   **`<PokerCard />`**: Visual representation of a card (suit colors, symbols).
*   **`<CardInput />`**: Interactive selector for choosing cards.
*   **`<EquityDisplay />`**: Circular progress or bar charts for win/loss percentages.
*   **`<RecommendationPanel />`**: Semantic alert showing the tool's advice.
*   **`<HistoryTable />`**: Tabular view of past rounds.

### Views (Web Pages)
1.  **Dashboard (`/`)**: The main "Live" view for inputting hands and seeing real-time analysis.
2.  **History (`/history`)**: Reviewing past sessions, rounds, and snapshots.
3.  **Settings (`/settings`)**: Configuring default NPC aggression and simulation iterations.

---

## 5. User Flows

### A. The Analyzer Flow (Real-time Play)
1.  **Session Init**: User opens the dashboard. A session is automatically checked/started.
2.  **Card Entry**: User selects Hole cards via `<CardInput />`.
3.  **Analysis**: User clicks "Analyze." The UI calls `POST /api/poker/analyze`.
4.  **Feedback**: The `<EquityDisplay />` and `<RecommendationPanel />` update instantly.
5.  **Recording**: If "Record" is toggled, the snapshot is saved.
6.  **Resolution**: Once the RDR2 hand ends, the user clicks "Win/Loss" to resolve the round.

### B. The Historian Flow (Reflection)
1.  **Browsing**: User navigates to `/history`.
2.  **Filtering**: User filters by "Valentine" or "Poker."
3.  **Inspection**: User clicks a Round ID to see the step-by-step snapshots (Flop -> Turn -> River).

---

## 6. Testing Strategy
We utilize **Vitest** for a unified testing experience that mirrors the Vite build environment.
*   **Unit Tests**: Logic verification (e.g., formatting card strings).
*   **Component Tests**: Verifying UI behavior (e.g., "Does the card turn red when a Heart is selected?").
*   **Mocking**: Axios is mocked to prevent real API calls during testing.

---

## 7. Containerization Strategy
To ensure a consistent environment across development and production, the frontend is containerized using a multi-stage Docker build.

### A. Docker Images & Services
*   **Build Stage (`node:18-alpine`)**:
    *   **Image**: A lightweight Node.js Alpine image.
    *   **Purpose**: Handles the compilation of Vue components and SASS into optimized static assets (HTML, CSS, JS).
    *   **Service**: This stage runs only during the image build process.
*   **Production Stage (`nginx:stable-alpine`)**:
    *   **Image**: A high-performance, stable Nginx Alpine image.
    *   **Purpose**: Serves the compiled static assets to the browser on port `8080`.
    *   **Service**: The long-running `frontend` container in our `docker-compose.yml`.

### B. Development Mode
During local development, we use **Vite's Dev Server** directly (usually through a separate dev-only container or local Node process) to take advantage of **Hot Module Replacement (HMR)**.

### C. Docker Context
*   **`docker/frontend.Dockerfile`**: Contains the multi-stage build instructions.
*   **`docker-compose.yml`**: Orchestrates the `frontend` service alongside the `backend` API.
