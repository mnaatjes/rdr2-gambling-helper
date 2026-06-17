<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps<{
  rank: string;
  suit: 'h' | 'd' | 's' | 'c';
  size?: 'sm' | 'md' | 'lg';
  hidden?: boolean;
}>();

const suitSymbol = computed(() => {
  const symbols = { h: '♥', d: '♦', s: '♠', c: '♣' };
  return symbols[props.suit];
});

const isRed = computed(() => ['h', 'd'].includes(props.suit));
</script>

<template>
  <div :class="['game-card', size || 'md', { 'is-red': isRed, 'is-hidden': hidden }]">
    <div v-if="!hidden" class="card-front">
      <div class="top-left">
        <span class="rank">{{ rank }}</span>
        <span class="suit">{{ suitSymbol }}</span>
      </div>
      <div class="center-suit">{{ suitSymbol }}</div>
      <div class="bottom-right">
        <span class="rank">{{ rank }}</span>
        <span class="suit">{{ suitSymbol }}</span>
      </div>
    </div>
    <div v-else class="card-back">
      <div class="pattern"></div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@import '../../assets/scss/variables';
@import '../../assets/scss/mixins';

.game-card {
  background-color: $parchment;
  color: $paper-ink;
  border-radius: 4px;
  position: relative;
  box-shadow: 2px 2px 8px rgba(0,0,0,0.5);
  transition: transform 0.2s ease;
  border: 1px solid rgba($paper-ink, 0.2);

  &.is-red .suit, &.is-red .rank {
    color: $blood-red;
  }

  &.sm { width: 50px; height: 75px; font-size: 0.8rem; .center-suit { font-size: 1.5rem; } }
  &.md { width: 80px; height: 120px; font-size: 1.2rem; .center-suit { font-size: 2.5rem; } }
  &.lg { width: 110px; height: 165px; font-size: 1.5rem; .center-suit { font-size: 3.5rem; } }

  .card-front {
    height: 100%;
    padding: $spacing-xs;
    display: flex;
    flex-direction: column;
    justify-content: space-between;

    .top-left, .bottom-right {
      display: flex;
      flex-direction: column;
      line-height: 1;
      font-weight: bold;
    }

    .bottom-right {
      transform: rotate(180deg);
    }

    .center-suit {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      opacity: 0.15;
    }
  }

  .card-back {
    height: 100%;
    background-color: $deep-crimson;
    border: 4px solid $parchment;
    border-radius: 2px;
    display: flex;
    align-items: center;
    justify-content: center;

    .pattern {
      width: 100%;
      height: 100%;
      background-image: radial-gradient($brass-gold 1px, transparent 1px);
      background-size: 10px 10px;
      opacity: 0.3;
    }
  }
}
</style>
