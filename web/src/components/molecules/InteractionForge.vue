<script setup lang="ts">
import { usePokerStore } from '../../store/poker';
import CentralDeck from '../atomic/CentralDeck.vue';

const store = usePokerStore();

const resolve = (outcome: 'win' | 'loss' | 'fold' | 'tie') => {
  store.resolveHand(outcome);
};
</script>

<template>
  <div class="interaction-forge">
    <!-- Stage Indicator HUD -->
    <div class="stage-hud">
      <div class="hud-status" :class="store.currentStage.toLowerCase().replace(' ', '-')">
        {{ store.currentStage }}
      </div>
    </div>

    <!-- Central Deck -->
    <div class="forge-main">
      <CentralDeck />
    </div>

    <!-- Actions Panel -->
    <div class="forge-actions">
      <!-- Loading State -->
      <div v-if="store.loading" class="status-panel loading">
        <div class="spinner"></div>
        <span class="hud-hint">Consulting the Odds...</span>
      </div>

      <!-- Error State with Retry -->
      <div v-else-if="store.error" class="status-panel error">
        <span class="error-msg">{{ store.error }}</span>
        <button class="action-btn retry" @click="store.runAnalysis()">Retry Analysis</button>
      </div>

      <!-- Resolution Panel (Active Game) -->
      <div class="resolution-panel" v-else-if="store.roundId">
        <button class="action-btn fold" @click="resolve('fold')">Fold</button>
        <button class="action-btn loss" @click="resolve('loss')">Lost</button>
        <button class="action-btn win" @click="resolve('win')">Won</button>
      </div>

      <!-- Awaiting State (Initial) -->
      <div class="awaiting-panel" v-else>
        <span class="hud-hint" v-if="store.allInPlayCards.length === 0">Awaiting Player Cards...</span>
        <span class="hud-hint" v-else-if="!store.isStageComplete">Finish selecting cards for {{ store.currentStage }}...</span>
        <button v-else class="action-btn analyze" @click="store.runAnalysis()">Analyze Hand</button>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '../../assets/scss/variables';
@import '../../assets/scss/mixins';

.interaction-forge {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
  height: 100%;
}

.stage-hud {
  @include hud-panel;
  text-align: center;
  padding: $spacing-sm;

  .hud-status {
    @include font-hud-condensed;
    font-size: 1.2rem;
    color: $brass-gold;
    transition: all 0.3s ease;

    &.awaiting { opacity: 0.5; color: $pure-white; }
    &.pre-flop, &.the-flop, &.the-turn, &.the-river {
      color: $iconic-red;
      text-shadow: 0 0 10px rgba($iconic-red, 0.4);
    }
  }
}

.forge-actions {
  @include hud-panel;
  margin-top: auto;
  min-height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.status-panel {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $spacing-sm;
  width: 100%;

  .error-msg {
    color: $iconic-red;
    @include font-hud-condensed;
    font-size: 0.9rem;
  }
}

.resolution-panel {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: $spacing-sm;
  width: 100%;
}

.action-btn {
  @include font-hud-condensed;
  padding: $spacing-sm $spacing-md;
  background: rgba($pure-black, 0.6);
  border: 1px solid $brass-gold;
  color: $pure-white;
  cursor: pointer;
  transition: all 0.2s ease;
  text-transform: uppercase;

  &:hover {
    background: $brass-gold;
    color: $pure-black;
  }

  &.analyze {
    width: 100%;
    background: rgba($iconic-red, 0.2);
    border-color: $iconic-red;
    color: $iconic-red;

    &:hover {
      background: $iconic-red;
      color: $pure-white;
    }
  }

  &.retry {
    font-size: 0.8rem;
    padding: $spacing-xs $spacing-sm;
  }
}

.spinner {
  width: 20px;
  height: 20px;
  border: 2px solid rgba($brass-gold, 0.3);
  border-top-color: $brass-gold;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.action-btn {
  @include font-hud-condensed;
  padding: $spacing-sm;
  border: 1px solid rgba($pure-white, 0.2);
  color: $pure-white;
  font-size: 0.9rem;
  transition: all 0.2s;

  &:hover {
    border-color: $brass-gold;
    background: rgba($brass-gold, 0.1);
  }

  &.fold { border-color: rgba($blood-red, 0.5); color: $blood-red; }
  &.win { border-color: rgba($sunburst, 0.5); color: $sunburst; }
}

.hud-hint {
  @include font-hud-condensed;
  font-size: 0.8rem;
  opacity: 0.6;
  display: block;
  text-align: center;
}

.forge-error {
  color: $blood-red;
  font-size: 0.8rem;
  text-align: center;
  @include font-hud-condensed;
}
</style>
