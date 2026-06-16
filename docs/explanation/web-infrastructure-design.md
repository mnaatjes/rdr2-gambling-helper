---
title: Web UI Infrastructure Design
tags: [architecture, web, api, docker, flask, networking]
created-at: 2026-06-16
updated-at: 2026-06-16
---

# Web UI Infrastructure Design Document

## 1. Overview
This document outlines the transition of the RDR2 Gambling Utility from a local CLI-only tool to a containerized, client-server web application. This architecture ensures that the core gambling logic remains shared between the CLI and the new Web UI.

## 2. Planned Directory Structure (Monorepo)
The project will follow a monorepo pattern to keep logic, services, and frontend code in a single, version-controlled environment.

```text
rdr2-gambler/
├── src/                # THE CORE (Service A & B)
│   ├── core/           # Game Logic, History Service, Data Models
│   ├── cli/            # CLI implementation (Thin Client)
│   └── api/            # <--- NEW: Flask API wrapper for Web/External use
├── web/                # <--- NEW: The Frontend UI (Framework TBD)
│   ├── src/
│   ├── public/
│   └── package.json
├── docker/             # <--- NEW: Dockerfiles for each service
│   ├── backend.Dockerfile
│   └── frontend.Dockerfile
├── docker-compose.yml  # <--- NEW: Orchestration
├── pyproject.toml
└── README.md
```

## 3. Service & Container Strategy

We will utilize **Docker Compose** to manage the following services:

### A. Backend API (`src/api/`)
*   **Role**: Acts as the bridge between the browser and the Python gambling logic.
*   **Framework**: **Flask**.
*   **Responsibilities**:
    *   Expose REST endpoints for poker/blackjack analysis.
    *   Interface with the `HistoryService` to record snapshots.
    *   Serve as the gatekeeper for the SQLite database.
*   **Internal Port**: `5000`

### B. Frontend Client (`web/`)
*   **Role**: User interface for manual entry and visual dashboards.
*   **Framework**: TBD (Options: Vue.js, VitePress, etc.).
*   **Responsibilities**:
    *   Capture user input (cards, table state).
    *   Consume the Backend API.
    *   Render high-fidelity game visualizations.
*   **Internal Port**: `5173` (Standard for Vite-based projects) or `3000`.

### C. Database Persistence
*   **Role**: Persistent storage for sessions and hand history.
*   **Current State**: SQLite.
*   **Docker Strategy**: The SQLite `.db` file will be mounted as a **Docker Volume** to ensure data persists even if the containers are destroyed.

---

## 4. Networking & Ports

### Planned Port Allocation
| Service | External Port | Internal Port | Protocol |
| :--- | :--- | :--- | :--- |
| **Frontend UI** | `8080` | `5173` | HTTP |
| **Backend API** | `5000` | `5000` | HTTP |

### Firewall Configuration (`ufw`)
Before implementation, the following ports must be allowed on the host machine:
```bash
sudo ufw allow 8080/tcp  # Frontend Access
sudo ufw allow 5000/tcp  # Backend API Access
```

---

## 5. Implementation Roadmap

1.  **Phase 1: API Scaffolding**: Implement the Flask wrapper in `src/api/` that mirrors the functionality of `PokerService`.
2.  **Phase 2: Dockerization**: Create `backend.Dockerfile` and `docker-compose.yml` to run the API and Database.
3.  **Phase 3: Frontend Choice & Scaffold**: Select the UI framework and initialize the `web/` directory.
4.  **Phase 4: Orchestration**: Finalize `docker-compose.yml` to link the Frontend and Backend services.

---

## 6. Port Availability Check
*Reminder: Before binding ports, we must verify availability using:*
```bash
netstat -tuln | grep -E '5000|8080'
```
