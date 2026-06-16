<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  rank: string;
  suit: 'h' | 'd' | 's' | 'c';
  size?: 'sm' | 'md' | 'lg';
}>();

const suitSymbol = computed(() => {
  const symbols = { h: '♥', d: '♦', s: '♠', c: '♣' };
  return symbols[props.suit];
});

const isRed = computed(() => ['h', 'd'].includes(props.suit));
</script>

<template>
  <div :class="['game-card', size || 'md', { 'is-red': isRed }]">
    <div class="card-content">
      <span class="rank">{{ rank }}</span>
      <span class="suit">{{ suitSymbol }}</span>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '../../assets/scss/variables';

.game-card {
  background-color: $pure-white;
  color: $rich-black;
  border-radius: 4px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  box-shadow: 0 2px 5px rgba(0,0,0,0.3);
  user-select: none;
  border: 1px solid #ccc;

  &.is-red {
    color: $deep-red;
  }

  &.sm { width: 40px; height: 60px; font-size: 1rem; }
  &.md { width: 60px; height: 90px; font-size: 1.5rem; }
  &.lg { width: 80px; height: 120px; font-size: 2rem; }

  .card-content {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
}
</style>
