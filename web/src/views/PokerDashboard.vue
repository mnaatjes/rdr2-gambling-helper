<script setup lang="ts">
import InteractionForge from '../components/molecules/InteractionForge.vue';
import GameTable from '../components/molecules/GameTable.vue';
import { RouterLink } from 'vue-router';
</script>

<template>
  <div class="poker-dashboard">
    <header class="dashboard-header">
      <RouterLink to="/" class="back-link">&larr; Return to Saloon</RouterLink>
      <h1>Texas Hold'em Assistant</h1>
    </header>

    <div class="dashboard-layout">
      <!-- Section A: Input Forge -->
      <aside class="side-panel">
        <InteractionForge />
      </aside>

      <!-- Section B: Game Table Display -->
      <main class="main-display">
        <GameTable />
      </main>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '../assets/scss/variables';
@import '../assets/scss/mixins';

.poker-dashboard {
  height: 100vh;
  display: flex;
  flex-direction: column;
  padding: $spacing-md;
  background-color: $rich-black;
}

.dashboard-header {
  display: flex;
  align-items: center;
  gap: $spacing-lg;
  margin-bottom: $spacing-md;

  .back-link {
    @include font-hud-condensed;
    color: $brass-gold;
    text-decoration: none;
    font-size: 0.9rem;
    &:hover { color: $pure-white; }
  }

  h1 {
    font-size: 2rem;
    margin: 0;
  }
}

.dashboard-layout {
  flex: 1;
  display: grid;
  grid-template-columns: 350px 1fr;
  gap: $spacing-md;
  min-height: 0; // Crucial for flex child to allow inner scroll
}

.side-panel {
  overflow-y: auto;
}

.main-display {
  min-height: 0; // Allow inner GameTable to scroll if needed
}

@media (max-width: 1024px) {
  .poker-dashboard { height: auto; overflow: visible; }
  .dashboard-layout {
    grid-template-columns: 1fr;
    overflow: visible;
  }
  .side-panel { order: 2; }
  .main-display { order: 1; min-height: 500px; }
}
</style>
