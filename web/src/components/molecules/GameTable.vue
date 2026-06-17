<script setup lang="ts">
import { computed } from 'vue';
import { usePokerStore } from '../../store/poker';
import GameCard from '../atomic/GameCard.vue';

const store = usePokerStore();

const parseCard = (s: string) => {
  if (s.length === 3) return { rank: s.slice(0, 2), suit: s.slice(2) as any };
  return { rank: s[0], suit: s[1] as any };
};

// Strip [bold blue] etc from the CLI-style response
const cleanRecommendation = computed(() => {
  if (!store.result?.recommendation) return '';
  return store.result.recommendation.replace(/\[\/?.*?\]/g, '');
});

const recColor = computed(() => {
  const rec = store.result?.recommendation || '';
  if (rec.includes('green')) return '#2ecc71';
  if (rec.includes('yellow')) return '#f1c40f';
  if (rec.includes('blue')) return '#3498db';
  return '#e74c3c';
});
</script>

<template>
  <div class="game-table-display">
    <div class="felt-surface">
      <div class="table-content">
        <!-- Player Hand -->
        <div class="hand-display player">
          <h4>Your Hand</h4>
          <div class="cards">
            <GameCard 
              v-for="c in store.hole" 
              :key="c" 
              v-bind="parseCard(c)" 
              size="lg" 
            />
            <div 
              v-for="_i in (2 - store.hole.length)" 
              class="placeholder lg error-highlight"
              :key="'hole-empty-' + _i"
            >
              <span>Required</span>
            </div>
          </div>
        </div>

        <!-- Community Cards -->
        <div class="hand-display community">
          <h4>Community Board</h4>
          <div class="cards">
            <GameCard 
              v-for="c in store.community" 
              :key="c" 
              v-bind="parseCard(c)" 
              size="md" 
            />
            <div 
              v-for="_i in (5 - store.community.length)" 
              class="placeholder md"
              :key="'comm-empty-' + _i"
            ></div>
          </div>
        </div>

        <!-- Results Area -->
        <div class="analysis-results" v-if="store.result">
          <div class="result-header">
            <span class="hand-name">{{ store.result.hand_name }}</span>
            <span class="round-id" v-if="store.roundId">#{{ store.roundId }}</span>
          </div>

          <div class="equity-cores">
            <div class="core win">
              <div class="ring" :style="{ '--p': store.result.win_rate * 100 }">
                <span class="val">{{ Math.round(store.result.win_rate * 100) }}%</span>
              </div>
              <label>Win</label>
            </div>
            <div class="core tie">
              <div class="ring" :style="{ '--p': store.result.tie_rate * 100 }">
                <span class="val">{{ Math.round(store.result.tie_rate * 100) }}%</span>
              </div>
              <label>Tie</label>
            </div>
            <div class="core loss">
              <div class="ring" :style="{ '--p': store.result.loss_rate * 100 }">
                <span class="val">{{ Math.round(store.result.loss_rate * 100) }}%</span>
              </div>
              <label>Loss</label>
            </div>
          </div>

          <div class="recommendation-bar" :style="{ color: recColor }">
            {{ cleanRecommendation }}
          </div>
        </div>

        <!-- Error Area -->
        <div class="error-results" v-if="store.error">
          <div class="error-header">Communication Failure</div>
          <div class="error-msg">{{ store.error }}</div>
        </div>

        <div class="loading-overlay" v-if="store.loading">
          <div class="shuffling-text">Simulating Hand...</div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '../../assets/scss/variables';
@import '../../assets/scss/mixins';

.game-table-display {
  @include game-table;
  height: 100%;
  border-radius: 8px;
  padding: $spacing-md;
}

.felt-surface {
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  align-items: center;
  overflow-y: auto;
  padding: $spacing-lg 0;

  &::-webkit-scrollbar {
    width: 6px;
  }
  &::-webkit-scrollbar-track {
    background: rgba(0, 0, 0, 0.2);
  }
  &::-webkit-scrollbar-thumb {
    background: $brass-gold;
    border-radius: 3px;
  }
}

.table-content {
  width: 100%;
  max-width: 800px;
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
  position: relative;
}

.hand-display {
  text-align: center;
  h4 { 
    @include font-hud-condensed; 
    color: rgba($pure-white, 0.4); 
    margin-bottom: $spacing-xs;
    font-size: 0.9rem;
  }
  .cards {
    display: flex;
    gap: $spacing-md;
    justify-content: center;
    min-height: 100px;
  }
}

.placeholder {
  width: 80px; height: 120px;
  border: 2px dashed rgba($pure-white, 0.2);
  border-radius: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-family: $font-hud;
  font-size: 0.7rem;
  color: rgba($pure-white, 0.2);
  text-transform: uppercase;

  &.lg { width: 80px; height: 120px; }
  &.md { width: 60px; height: 90px; }

  &.error-highlight {
    background: rgba($iconic-red, 0.1);
    border-color: rgba($iconic-red, 0.4);
    color: rgba($iconic-red, 0.6);
    box-shadow: 0 0 10px rgba($iconic-red, 0.2);
  }
}

.analysis-results {
  @include hud-panel;
  margin-top: $spacing-lg;
  animation: slide-up 0.3s ease-out;

  .result-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: $spacing-lg;
    .hand-name { @include font-branding; font-size: 1.8rem; }
    .round-id { color: $brass-gold; font-family: monospace; font-size: 0.8rem; }
  }
}

.error-results {
  @include hud-panel;
  margin-top: $spacing-lg;
  border-color: $iconic-red;
  text-align: center;

  .error-header {
    @include font-hud-condensed;
    @include ink-bleed($iconic-red);
    font-size: 1.5rem;
    margin-bottom: $spacing-sm;
  }
  .error-msg {
    color: rgba($pure-white, 0.8);
    font-size: 0.9rem;
  }
}

.equity-cores {
  display: flex;
  justify-content: space-around;
  margin-bottom: $spacing-lg;

  .core {
    text-align: center;
    label { @include font-hud-condensed; display: block; margin-top: $spacing-xs; }
  }

  .ring {
    width: 70px; height: 70px;
    border-radius: 50%;
    border: 4px solid rgba($pure-white, 0.1);
    display: flex;
    align-items: center;
    justify-content: center;
    position: relative;
    background: radial-gradient(closest-side, transparent 80%, rgba(255,255,255,0.1) 100%);
    
    &::after {
      content: '';
      position: absolute;
      top: -4px; left: -4px; right: -4px; bottom: -4px;
      border-radius: 50%;
      border: 4px solid transparent;
      border-top-color: $brass-gold;
      transform: rotate(calc(var(--p) * 3.6deg));
    }

    .val { font-family: $font-hud; font-size: 1.2rem; }
  }
}

.recommendation-bar {
  background: rgba(0,0,0,0.5);
  padding: $spacing-md;
  text-align: center;
  border-top: $border-brass;
  border-bottom: $border-brass;
  font-family: $font-hud;
  font-size: 1.5rem;
}

.loading-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba($rich-black, 0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 10;
  .shuffling-text { @include font-hud-condensed; font-size: 2rem; color: $sunburst; }
}

@keyframes slide-up { from { opacity: 0; transform: translateY(20px); } to { opacity: 1; transform: translateY(0); } }
</style>
