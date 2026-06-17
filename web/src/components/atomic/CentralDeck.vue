<script setup lang="ts">
import { usePokerStore } from '../../store/poker';

const store = usePokerStore();

const ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2'];
const suits = [
  { val: 's', symbol: '♠', name: 'Spades', color: 'white' },
  { val: 'h', symbol: '♥', name: 'Hearts', color: 'red' },
  { val: 'd', symbol: '♦', name: 'Diamonds', color: 'red' },
  { val: 'c', symbol: '♣', name: 'Clubs', color: 'white' },
];

const handleDragStart = (event: DragEvent, card: string) => {
  if (event.dataTransfer) {
    event.dataTransfer.setData('card', card);
    event.dataTransfer.effectAllowed = 'move';
  }
};

const isInPlay = (rank: string, suit: string) => {
  return store.allInPlayCards.includes(`${rank}${suit}`);
};
</script>

<template>
  <div class="central-deck">
    <div class="deck-header">
      <span class="hud-label">Central Deck</span>
    </div>
    <div class="deck-grid">
      <div v-for="suit in suits" :key="suit.val" class="suit-row">
        <div 
          v-for="rank in ranks" 
          :key="rank"
          :class="['card-item', suit.color, { 'in-play': isInPlay(rank, suit.val) }]"
          :draggable="!isInPlay(rank, suit.val)"
          @dragstart="handleDragStart($event, `${rank}${suit.val}`)"
        >
          <span class="rank">{{ rank }}</span>
          <span class="suit">{{ suit.symbol }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '../../assets/scss/variables';
@import '../../assets/scss/mixins';

.central-deck {
  @include hud-panel;
  background: rgba(0, 0, 0, 0.4);
  padding: $spacing-sm;
}

.deck-header {
  margin-bottom: $spacing-sm;
  text-align: center;
  border-bottom: $border-distressed;
  padding-bottom: $spacing-xs;

  .hud-label {
    @include font-hud-condensed;
    font-size: 0.8rem;
    color: $brass-gold;
  }
}

.deck-grid {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.suit-row {
  display: flex;
  gap: 4px;
  justify-content: center;
}

.card-item {
  width: 28px;
  height: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 0.7rem;
  background: #2a2a2a;
  border: 1px solid #444;
  border-radius: 2px;
  cursor: grab;
  transition: all 0.2s ease;
  user-select: none;

  &.red { color: $blood-red; }
  &.white { color: #eee; }

  &:hover:not(.in-play) {
    border-color: $brass-gold;
    background: #333;
    transform: translateY(-2px);
    box-shadow: 0 2px 8px rgba(0,0,0,0.5);
  }

  &.in-play {
    opacity: 0.15;
    cursor: not-allowed;
    filter: grayscale(1);
  }

  .rank { font-weight: bold; line-height: 1; }
  .suit { font-size: 0.9rem; }
}

@media (max-width: 1200px) {
  .card-item { width: 22px; height: 32px; font-size: 0.6rem; }
}
</style>
