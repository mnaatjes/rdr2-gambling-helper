<script setup lang="ts">
import { usePokerStore } from '../../store/poker';
import CardSelector from '../atomic/CardSelector.vue';
import GameButton from '../atomic/GameButton.vue';

const store = usePokerStore();

const toggleHole = (card: string) => {
  if (store.hole.includes(card)) {
    store.hole = store.hole.filter(c => c !== card);
  } else if (store.hole.length < 2) {
    store.hole.push(card);
  }
};

const toggleCommunity = (card: string) => {
  if (store.community.includes(card)) {
    store.community = store.community.filter(c => c !== card);
  } else if (store.community.length < 5) {
    store.community.push(card);
  }
};
</script>

<template>
  <div class="interaction-forge">
    <section class="forge-section">
      <h3><span class="step">1</span> Hole Cards</h3>
      <CardSelector :active-cards="store.hole" @select="toggleHole" />
    </section>

    <section class="forge-section">
      <h3><span class="step">2</span> Community Cards</h3>
      <CardSelector :active-cards="store.community" @select="toggleCommunity" />
    </section>

    <section class="forge-section settings">
      <h3><span class="step">3</span> Environment</h3>
      <div class="field">
        <label>Opponents: {{ store.opponents }}</label>
        <input type="range" v-model.number="store.opponents" min="1" max="7" step="1" />
      </div>
      <div class="field">
        <label>NPC Aggression: {{ store.aggression }}</label>
        <input type="range" v-model.number="store.aggression" min="0.1" max="1.0" step="0.1" />
      </div>
      <div class="field toggle">
        <label>Record Hand History</label>
        <input type="checkbox" v-model="store.recording" />
      </div>
    </section>

    <div class="actions">
      <GameButton 
        label="Analyze Hand" 
        variant="primary" 
        @click="store.runAnalysis()" 
        :disabled="store.hole.length < 2"
      />
      <GameButton 
        label="Reset Table" 
        variant="secondary" 
        @click="store.clearHand()" 
      />
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '../../assets/scss/variables';
@import '../../assets/scss/mixins';

.interaction-forge {
  @include hud-panel;
  display: flex;
  flex-direction: column;
  gap: $spacing-lg;
  height: 100%;
}

.forge-section {
  h3 {
    @include font-hud-condensed;
    font-size: 1.2rem;
    color: $sunburst;
    margin-bottom: $spacing-sm;
    display: flex;
    align-items: center;
    gap: $spacing-sm;

    .step {
      width: 20px;
      height: 20px;
      background: $brass-gold;
      color: $rich-black;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 0.8rem;
    }
  }
}

.settings {
  .field {
    margin-bottom: $spacing-md;
    label {
      display: block;
      @include font-hud-condensed;
      font-size: 0.9rem;
      margin-bottom: 2px;
    }
    input[type="range"] {
      width: 100%;
      accent-color: $iconic-red;
    }
  }
  .toggle {
    display: flex;
    justify-content: space-between;
    align-items: center;
    input { width: auto; }
  }
}

.actions {
  display: flex;
  flex-direction: column;
  gap: $spacing-sm;
  margin-top: auto;
}
</style>
