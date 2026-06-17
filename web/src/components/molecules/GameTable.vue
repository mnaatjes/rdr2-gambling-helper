<script setup lang="ts">
import { usePokerStore } from '../../store/poker';
import InteractiveCardSlot from '../atomic/InteractiveCardSlot.vue';
import { computed } from 'vue';

const store = usePokerStore();

const formatPercentage = (val: number) => {
  return `${(val * 100).toFixed(1)}%`;
};

const recColorClass = computed(() => {
  if (!store.result) return '';
  const wr = store.result.win_rate;
  if (wr > 0.7) return 'is-green';
  if (wr > 0.4) return 'is-yellow';
  if (wr > 0.2) return 'is-blue';
  return 'is-red';
});
</script>

<template>
  <div class="game-table">
    <div class="table-surface">
      <!-- Community Cards Section -->
      <div class="community-section">
        <div class="section-label">Community Pot</div>
        <div class="slots-container">
          <InteractiveCardSlot 
            v-for="(_, i) in store.community" 
            :key="`comm-${i}`"
            section="community"
            :index="i"
          />
        </div>
      </div>

      <!-- Player Cards Section -->
      <div class="player-section">
        <div class="section-label">Your Hand</div>
        <div class="slots-container">
          <InteractiveCardSlot 
            v-for="(_, i) in store.hole" 
            :key="`hole-${i}`"
            section="hole"
            :index="i"
          />
        </div>
      </div>
    </div>

    <!-- Analysis Dashboard Overlay -->
    <div v-if="store.result" class="analysis-overlay">
      <div class="result-card">
        <div class="hand-name">{{ store.result.hand_name }}</div>
        <div class="odds-grid">
          <div class="odd-item">
            <span class="label">Win Rate</span>
            <span class="value win">{{ formatPercentage(store.result.win_rate) }}</span>
          </div>
          <div class="odd-item">
            <span class="label">Tie Rate</span>
            <span class="value tie">{{ formatPercentage(store.result.tie_rate) }}</span>
          </div>
        </div>
        <div 
          class="recommendation"
          :class="recColorClass"
        >
          {{ store.result.recommendation }}
        </div>
      </div>
    </div>
    
    <div v-if="store.loading" class="loading-overlay">
      <span class="hud-label">Simulating Odds...</span>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '../../assets/scss/variables';
@import '../../assets/scss/mixins';

.game-table {
  @include game-table;
  width: 90%;
  max-width: 1000px;
  margin: 0 auto;
  min-height: 450px;
  position: relative;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: $spacing-lg;
  overflow: hidden;
}

.table-surface {
  display: flex;
  flex-direction: column;
  gap: $spacing-xl;
  align-items: center;
  width: 100%;
}

.section-label {
  @include font-hud-condensed;
  font-size: 0.8rem;
  color: rgba($pure-white, 0.4);
  text-align: center;
  margin-bottom: $spacing-sm;
  letter-spacing: 2px;
}

.slots-container {
  display: flex;
  gap: $spacing-md;
  justify-content: center;
}

.analysis-overlay {
  position: absolute;
  top: $spacing-md;
  right: $spacing-md;
  width: 250px;
  @include hud-panel;
  z-index: 10;
}

.result-card {
  .hand-name {
    @include font-branding;
    font-size: 1.4rem;
    margin-bottom: $spacing-sm;
    text-align: center;
  }

  .odds-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: $spacing-sm;
    margin-bottom: $spacing-md;
    border-top: $border-distressed;
    padding-top: $spacing-sm;
  }

  .odd-item {
    display: flex;
    flex-direction: column;
    align-items: center;

    .label { @include font-hud-condensed; font-size: 0.7rem; opacity: 0.6; }
    .value { font-size: 1.1rem; font-weight: bold; }
    .win { color: $sunburst; }
    .tie { color: $pure-white; }
  }

  .recommendation {
    @include font-hud-condensed;
    padding: $spacing-sm;
    text-align: center;
    color: $pure-white;
    font-size: 0.9rem;
    letter-spacing: 1px;
    border: 1px solid transparent;

    &.is-green { background: rgba(#2ecc71, 0.15); border-color: rgba(#2ecc71, 0.3); }
    &.is-yellow { background: rgba($sunburst, 0.15); border-color: rgba($sunburst, 0.3); }
    &.is-blue { background: rgba(#3498db, 0.15); border-color: rgba(#3498db, 0.3); }
    &.is-red { background: rgba($iconic-red, 0.15); border-color: rgba($iconic-red, 0.3); }
  }
}

.loading-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  backdrop-filter: blur(2px);
  z-index: 20;

  .hud-label { @include font-hud-condensed; font-size: 1.5rem; color: $brass-gold; }
}

@media (max-width: 1024px) {
  .game-table { border-radius: 12px; height: auto; padding: $spacing-lg; }
  .analysis-overlay { position: static; width: 100%; margin-top: $spacing-md; }
}
</style>
