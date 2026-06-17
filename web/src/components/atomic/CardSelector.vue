<script setup lang="ts">
const emit = defineProps<{
  activeCards: string[];
}>();

const emitSelect = defineEmits(['select']);

const ranks = ['A', 'K', 'Q', 'J', '10', '9', '8', '7', '6', '5', '4', '3', '2'];
const suits = [
  { val: 's', symbol: '♠', name: 'Spades', color: 'white' },
  { val: 'h', symbol: '♥', name: 'Hearts', color: 'red' },
  { val: 'd', symbol: '♦', name: 'Diamonds', color: 'red' },
  { val: 'c', symbol: '♣', name: 'Clubs', color: 'white' },
];

const selectCard = (rank: string, suit: string) => {
  const card = `${rank}${suit}`;
  emitSelect('select', card);
};

const isSelected = (rank: string, suit: string) => {
  return emit.activeCards.includes(`${rank}${suit}`);
};
</script>

<template>
  <div class="card-selector">
    <div v-for="suit in suits" :key="suit.val" class="suit-row">
      <button 
        v-for="rank in ranks" 
        :key="rank"
        :class="['card-btn', suit.color, { selected: isSelected(rank, suit.val) }]"
        @click="selectCard(rank, suit.val)"
      >
        <span class="rank">{{ rank }}</span>
        <span class="suit">{{ suit.symbol }}</span>
      </button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '../../assets/scss/variables';

.card-selector {
  display: flex;
  flex-direction: column;
  gap: $spacing-xs;
  background: rgba(0,0,0,0.3);
  padding: $spacing-sm;
  border-radius: 4px;
}

.suit-row {
  display: flex;
  gap: $spacing-xs;
  justify-content: center;
}

.card-btn {
  width: 32px;
  height: 45px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  font-size: 0.8rem;
  background: #2a2a2a;
  color: #ccc;
  border: 1px solid #444;
  border-radius: 2px;
  padding: 0;

  &.red { color: $blood-red; }
  &.white { color: #eee; }

  &.selected {
    background: $brass-gold;
    color: $rich-black;
    border-color: $pure-white;
    transform: scale(1.1);
    z-index: 2;
  }

  &:hover:not(.selected) {
    background: #333;
    border-color: $brass-gold;
  }

  .rank { font-weight: bold; line-height: 1; }
  .suit { font-size: 1rem; }
}

@media (max-width: 600px) {
  .card-btn { width: 25px; height: 35px; font-size: 0.6rem; .suit { font-size: 0.8rem; } }
}
</style>
