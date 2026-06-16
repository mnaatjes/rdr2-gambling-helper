<script setup lang="ts">
defineProps<{
  label: string;
  variant?: 'primary' | 'secondary' | 'brass';
}>();
</script>

<template>
  <button :class="['game-button', variant || 'primary']">
    <span class="label">{{ label }}</span>
  </button>
</template>

<style lang="scss" scoped>
@import '../../assets/scss/variables';
@import '../../assets/scss/mixins';

.game-button {
  padding: $spacing-sm $spacing-lg;
  font-family: $font-hud;
  text-transform: uppercase;
  font-size: 1.2rem;
  letter-spacing: 1px;
  transition: all 0.2s ease;
  border-radius: 2px;
  position: relative;
  overflow: hidden;

  &.primary {
    background-color: $primary-red;
    color: $pure-white;
    &:hover { background-color: lighten($primary-red, 10%); }
  }

  &.secondary {
    background-color: $rich-black;
    color: $pure-white;
    border: 1px solid $primary-red;
    &:hover { background-color: rgba($primary-red, 0.1); }
  }

  &.brass {
    background-color: $brass-gold;
    color: $pure-white;
    &:hover { background-color: lighten($brass-gold, 10%); }
  }

  &:active {
    transform: translateY(2px);
  }
}
</style>
