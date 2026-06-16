---
title: How to Setup Frontend Tooling
tags: [setup, node, sass, vite, vue]
created-at: 2026-06-16
updated-at: 2026-06-16
---

# How to Setup Frontend Tooling

This guide explains how to install and incorporate the Node.js and SASS tooling required for the Vue.js frontend.

## 1. Prerequisites
Ensure you have **Node.js (v18+)** and **npm** installed. We recommend using `nvm` (Node Version Manager).

## 2. Initializing the Project
From the project root, initialize the `web/` directory using Vite:
```bash
npm create vite@latest web -- --template vue
cd web
npm install
```

## 3. Incorporating SASS
We use the modern `sass-embedded` package for high-performance CSS pre-processing.

### Installation
```bash
npm install -D sass-embedded
```

### Usage in Components
To use SASS in a Vue component, add `lang="scss"` to the style tag:
```vue
<style lang="scss" scoped>
$poker-red: #e74c3c;

.card-heart {
  color: $poker-red;
  font-weight: bold;
}
</style>
```

## 4. Incorporating API Client (Axios)
Axios handles communication with our Flask Backend.

### Installation
```bash
npm install axios
```

### Configuration (`src/services/api.js`)
Create a centralized client to handle the base URL:
```javascript
import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:5000/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

export default apiClient;
```

## 5. Running the Development Server
To start the interactive development environment with Hot Module Replacement (HMR):
```bash
npm run dev
```
The UI will be available at `http://localhost:5173`.
