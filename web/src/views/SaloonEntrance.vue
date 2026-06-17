<script setup lang="ts">
import GameButton from '../components/atomic/GameButton.vue';
import { RouterLink } from 'vue-router';
</script>

<template>
  <div class="saloon-entrance">
    <div class="vignette"></div>
    
    <header class="hero">
      <h1 class="main-title">Red Dead Redemption 2</h1>
      <p class="subtitle">Gambling Utility Assistant</p>
    </header>

    <main class="game-selection container">
      <div class="game-grid">
        <div class="game-tile">
          <div class="tile-content">
            <span class="ornament"></span>
            <div class="tile-icon">🎴</div>
            <h2>Texas Hold'em</h2>
            <p>Real-time equity analysis & NPC behavior prediction.</p>
            <RouterLink to="/poker">
              <GameButton label="Enter Poker Room" variant="primary" />
            </RouterLink>
          </div>
        </div>

        <div class="game-tile">
          <div class="tile-content">
            <span class="ornament"></span>
            <div class="tile-icon">🃏</div>
            <h2>Blackjack</h2>
            <p>Dealer bust rates & optimal strategy guides.</p>
            <GameButton label="Join Table" variant="secondary" />
          </div>
        </div>

        <div class="game-tile">
          <div class="tile-content">
            <span class="ornament"></span>
            <div class="tile-icon">📜</div>
            <h2>The Ledger</h2>
            <p>Review your gambling history and track profits.</p>
            <GameButton label="Open Journal" variant="brass" />
          </div>
        </div>
      </div>
    </main>

    <footer class="legal">
      <p>Est. 1899 &bull; Van der Linde Gang Enterprises</p>
    </footer>
  </div>
</template>

<style lang="scss" scoped>
@import '../assets/scss/variables';
@import '../assets/scss/mixins';

.saloon-entrance {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
  position: relative;
  background-color: $rich-black;
  overflow-x: hidden;
}

.vignette {
  position: fixed;
  top: 0; left: 0; width: 100%; height: 100%;
  box-shadow: inset 0 0 200px rgba(0,0,0,0.5);
  pointer-events: none;
  z-index: 1;
}

.hero {
  text-align: center;
  padding: $spacing-xl 0;
  z-index: 2;
  
  .main-title {
    @include font-branding;
    font-size: 4rem;
    margin-bottom: $spacing-xs;
  }

  .subtitle {
    @include font-hud-condensed;
    color: $sunburst;
    font-size: 1.8rem;
    letter-spacing: 4px;
  }
}

.game-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: $spacing-xl;
  margin-top: $spacing-lg;
  z-index: 2;
}

.game-tile {
  @include hud-panel;
  padding: 2px; // Space for outer border
  transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);

  &:hover {
    transform: translateY(-10px) scale(1.02);
    border-color: $iconic-red;
    
    .ornament { background-color: $iconic-red; }
  }

  .tile-content {
    background: rgba($rich-black, 0.5);
    padding: $spacing-lg;
    height: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: $spacing-md;
    text-align: center;
    position: relative;
  }

  .ornament {
    width: 60px;
    height: 2px;
    background-color: $brass-gold;
    margin-bottom: $spacing-sm;
    transition: background-color 0.3s;
  }

  .tile-icon {
    font-size: 4.5rem;
    margin-bottom: $spacing-sm;
    filter: drop-shadow(0 4px 10px rgba(0,0,0,0.5));
  }

  h2 {
    @include font-hud-condensed;
    font-size: 2.2rem;
    color: $pure-white;
  }

  p {
    font-family: $font-body;
    font-size: 1.1rem;
    color: rgba($pure-white, 0.7);
    min-height: 4rem;
  }
}

.legal {
  margin-top: auto;
  padding: $spacing-xl;
  text-align: center;
  z-index: 2;
  
  p {
    @include font-hud-condensed;
    font-size: 0.9rem;
    color: rgba($pure-white, 0.4);
    letter-spacing: 2px;
  }
}

@media (max-width: 768px) {
  .hero .main-title { font-size: 2.8rem; }
  .game-grid { grid-template-columns: 1fr; gap: $spacing-lg; }
  .game-tile { margin: 0 $spacing-md; }
}
</style>
