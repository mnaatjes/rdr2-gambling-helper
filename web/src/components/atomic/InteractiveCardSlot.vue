<script setup lang="ts">
import { computed } from 'vue';
import { usePokerStore } from '../../store/poker';

const props = defineProps<{
  section: 'hole' | 'community';
  index: number;
}>();

const store = usePokerStore();

const currentCard = computed(() => {
  return props.section === 'hole' 
    ? store.hole[props.index] 
    : store.community[props.index];
});

const isRequired = computed(() => {
  if (props.section === 'hole') {
    return store.requiredSlots.hole.includes(props.index);
  }
  return store.requiredSlots.community.includes(props.index);
});

const handleDrop = (event: DragEvent) => {
  const card = event.dataTransfer?.getData('card');
  if (card) {
    store.placeCard(props.section, props.index, card);
  }
};

const removeCard = () => {
  store.removeCard(props.section, props.index);
};

// Helper to parse card string "As" -> { rank: "A", suit: "s" }
const parsedCard = computed(() => {
  if (!currentCard.value) return null;
  const c = currentCard.value;
  if (c.length === 3) return { rank: '10', suit: c[2] };
  return { rank: c[0], suit: c[1] };
});

const suitSymbol = computed(() => {
  if (!parsedCard.value) return '';
  const symbols: any = { h: '♥', d: '♦', s: '♠', c: '♣' };
  return symbols[parsedCard.value.suit];
});
</script>

<template>
  <div 
    :class="['card-slot', { 'is-required': isRequired, 'has-card': !!currentCard }]"
    @dragover.prevent
    @drop="handleDrop"
  >
    <div v-if="currentCard" class="slotted-card" @click="removeCard">
      <div class="card-content" :class="{ 'is-red': ['h', 'd'].includes(parsedCard?.suit || '') }">
        <span class="rank">{{ parsedCard?.rank }}</span>
        <span class="suit">{{ suitSymbol }}</span>
      </div>
      <div class="remove-overlay">✕</div>
    </div>
    <div v-else class="slot-placeholder">
      <span v-if="isRequired" class="plus">+</span>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '../../assets/scss/variables';
@import '../../assets/scss/mixins';

.card-slot {
  width: 80px;
  height: 112px;
  background: rgba(0, 0, 0, 0.2);
  border: 2px dashed rgba($brass-gold, 0.3);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: all 0.3s ease;

  &.is-required {
    background: rgba($iconic-red, 0.1);
    border-color: rgba($iconic-red, 0.4);
    box-shadow: inset 0 0 10px rgba($iconic-red, 0.2);
    
    .plus {
      color: rgba($iconic-red, 0.4);
      font-size: 2rem;
      font-weight: bold;
    }
  }

  &.has-card {
    border-style: solid;
    border-color: $brass-gold;
    background: $parchment;
  }
}

.slotted-card {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  position: relative;

  .card-content {
    color: $paper-ink;
    display: flex;
    flex-direction: column;
    align-items: center;
    line-height: 1;

    &.is-red { color: $blood-red; }

    .rank { font-size: 1.8rem; font-weight: bold; }
    .suit { font-size: 2.2rem; }
  }

  &:hover .remove-overlay {
    opacity: 1;
  }
}

.remove-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba($blood-red, 0.8);
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  opacity: 0;
  transition: opacity 0.2s;
  border-radius: 10px;
}

@media (max-width: 1024px) {
  .card-slot { width: 40px; height: 56px; }
}
</style>
