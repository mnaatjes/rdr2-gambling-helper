<script setup lang="ts">
import GameButton from '../components/atomic/GameButton.vue';
</script>

<template>
  <div class="saloon-entrance">
    <header class="hero">
      <h1 class="main-title">Red Dead Redemption 2</h1>
      <p class="subtitle">Gambling Utility Assistant</p>
    </header>

    <main class="game-selection container">
      <div class="game-grid">
        <div class="game-tile">
          <div class="tile-icon">🎴</div>
          <h2>Texas Hold'em</h2>
          <p>Real-time equity analysis & NPC behavior prediction.</p>
          <GameButton label="Enter Poker Room" variant="primary" />
        </div>

        <div class="game-tile">
          <div class="tile-icon">🃏</div>
          <h2>Blackjack</h2>
          <p>Dealer bust rates & optimal strategy guides.</p>
          <GameButton label="Join Table" variant="secondary" />
        </div>

        <div class="game-tile">
          <div class="tile-icon">📜</div>
          <h2>The Ledger</h2>
          <p>Review your gambling history and track profits.</p>
          <GameButton label="Open Journal" variant="brass" />
        </div>
      </div>
    </main>

    <footer class="legal">
      <p>&copy; 1899 Van der Linde Gang Enterprises</p>
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
  background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), 
              url('https://images.unsplash.com/photo-1533134486753-c833f0ed4866?auto=format&fit=crop&q=80&w=2070') center/cover;
}

.hero {
  text-align: center;
  padding: $spacing-xl 0;
  
  .main-title {
    font-size: 3.5rem;
    margin-bottom: $spacing-xs;
    text-shadow: 2px 2px 10px rgba(0,0,0,0.8);
  }

  .subtitle {
    @include hud-text;
    color: $brass-gold;
    font-size: 1.5rem;
  }
}

.game-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: $spacing-lg;
  margin-top: $spacing-lg;
}

.game-tile {
  @include western-panel;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: $spacing-md;
  transition: transform 0.3s ease;

  &:hover {
    transform: scale(1.02);
    border-color: $primary-red;
  }

  .tile-icon {
    font-size: 4rem;
  }

  h2 {
    font-size: 2rem;
    color: $pure-white;
    margin-bottom: 0;
  }

  p {
    font-size: 1rem;
    color: rgba($pure-white, 0.8);
    min-height: 3rem;
  }
}

.legal {
  margin-top: auto;
  padding: $spacing-lg;
  text-align: center;
  @include hud-text;
  font-size: 0.8rem;
  color: rgba($pure-white, 0.5);
}

@media (max-width: 768px) {
  .hero .main-title { font-size: 2.5rem; }
  .game-grid { grid-template-columns: 1fr; }
}
</style>
