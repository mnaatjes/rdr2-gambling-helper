import { defineStore } from 'pinia';
import { pokerApi, type PokerAnalyzeResponse } from '../services/api';

export const usePokerStore = defineStore('poker', {
  state: () => ({
    hole: [] as string[],
    community: [] as string[],
    opponents: 1,
    aggression: 0.2,
    loading: false,
    error: null as string | null,
    result: null as PokerAnalyzeResponse | null,
    roundId: null as string | null,
    sessionId: null as string | null,
    recording: true,
  }),

  actions: {
    setHole(cards: string[]) { this.hole = cards; },
    setCommunity(cards: string[]) { this.community = cards; },
    
    async runAnalysis() {
      if (this.hole.length < 2) return;
      
      this.loading = true;
      this.error = null;
      try {
        const response = await pokerApi.analyze({
          hole: this.hole,
          community: this.community,
          opponents: this.opponents,
          aggression: new Array(this.opponents).fill(this.aggression),
          record: this.recording,
          round_id: this.roundId || undefined,
          session_id: this.sessionId || undefined
        });

        this.result = response;
        if (response.metadata?.round_id) {
          this.roundId = response.metadata.round_id;
        }
      } catch (error: any) {
        this.error = error.response?.data?.error || error.message || 'Unknown error occurred';
        console.error('Analysis failed:', this.error);
      } finally {
        this.loading = false;
      }
    },

    clearHand() {
      this.hole = [];
      this.community = [];
      this.result = null;
      this.roundId = null;
    }
  }
});
