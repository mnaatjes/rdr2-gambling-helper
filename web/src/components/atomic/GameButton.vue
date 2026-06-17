<script setup lang="ts">
defineProps<{
  label: string;
  variant?: 'primary' | 'secondary' | 'brass';
}>();
</script>

<template>
  <button :class="['game-button', variant || 'primary']">
    <div class="inner-border"></div>
    <span class="label">{{ label }}</span>
  </button>
</template>

<style lang="scss" scoped>
@import '../../assets/scss/variables';
@import '../../assets/scss/mixins';

.game-button {
  @include font-hud-condensed;
  padding: $spacing-sm $spacing-xl;
  font-size: 1.4rem;
  transition: all 0.1s ease;
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 1px;
  
  .inner-border {
    position: absolute;
    top: 2px; left: 2px; right: 2px; bottom: 2px;
    border: 1px solid rgba($pure-white, 0.2);
    pointer-events: none;
  }

  &.primary {
    background-color: $iconic-red;
    color: $pure-white;
    border: 1px solid darken($iconic-red, 15%);
    box-shadow: 0 4px 0 darken($iconic-red, 20%);
    
    &:hover { background-color: lighten($iconic-red, 5%); }
    &:active {
      transform: translateY(2px);
      box-shadow: 0 2px 0 darken($iconic-red, 20%);
    }
  }

  &.secondary {
    background-color: $hud-bg;
    color: $pure-white;
    border: $border-brass;
    &:hover { background-color: rgba($pure-white, 0.1); }
  }

  &.brass {
    background-color: $brass-gold;
    color: $pure-white;
    border: 1px solid darken($brass-gold, 15%);
    box-shadow: 0 4px 0 darken($brass-gold, 20%);
    
    &:hover:not(:disabled) { background-color: lighten($brass-gold, 5%); }
    &:active:not(:disabled) {
      transform: translateY(2px);
      box-shadow: 0 2px 0 darken($brass-gold, 20%);
    }
  }

  &:disabled {
    opacity: 0.5;
    filter: grayscale(1);
    cursor: not-allowed;
    box-shadow: none;
    transform: none;
  }
}
</style>
