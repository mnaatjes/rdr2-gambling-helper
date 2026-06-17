import { defineStore } from 'pinia';
import { pokerApi, type PokerAnalyzeResponse } from '../services/api';

export const usePokerStore = defineStore('poker', {
  state: () => ({
    hole: [null, null] as (string | null)[],
    community: [null, null, null, null, null] as (string | null)[],
    opponents: 1,
    aggression: 0.2,
    loading: false,
    error: null as string | null,
    result: null as PokerAnalyzeResponse | null,
    roundId: null as string | null,
    sessionId: null as string | null,
    recording: true,
  }),

  getters: {
    allInPlayCards(state): string[] {
      return [...state.hole, ...state.community].filter((c): c is string => c !== null);
    },
    
    currentStage(state): 'AWAITING' | 'PRE-FLOP' | 'THE FLOP' | 'THE TURN' | 'THE RIVER' {
      const holeCount = state.hole.filter(c => c !== null).length;
      const commCount = state.community.filter(c => c !== null).length;

      if (holeCount < 2) return 'AWAITING';
      if (commCount === 0) return 'PRE-FLOP';
      if (commCount === 3) return 'THE FLOP';
      if (commCount === 4) return 'THE TURN';
      if (commCount === 5) return 'THE RIVER';
      
      // Intermediate/Invalid states
      if (commCount > 0 && commCount < 3) return 'PRE-FLOP';
      if (commCount > 3 && commCount < 4) return 'THE FLOP';
      if (commCount > 4 && commCount < 5) return 'THE TURN';
      
      return 'PRE-FLOP';
    },

    requiredSlots(): { hole: number[], community: number[] } {
      const stage = (this as any).currentStage;
      if (stage === 'AWAITING') return { hole: [0, 1], community: [] };
      if (stage === 'PRE-FLOP') return { hole: [], community: [0, 1, 2] };
      if (stage === 'THE FLOP') return { hole: [], community: [3] };
      if (stage === 'THE TURN') return { hole: [], community: [4] };
      return { hole: [], community: [] };
    },

    isStageComplete(state): boolean {
      const holeCount = state.hole.filter(c => c !== null).length;
      const commCount = state.community.filter(c => c !== null).length;
      return (holeCount === 2) && [0, 3, 4, 5].includes(commCount);
    }
  },

  actions: {
    placeCard(section: 'hole' | 'community', index: number, card: string) {
      if (this.allInPlayCards.includes(card)) return;

      if (section === 'hole') {
        this.hole[index] = card;
      } else {
        this.community[index] = card;
      }
      
      if (this.isStageComplete) {
        this.runAnalysis();
      }
    },

    removeCard(section: 'hole' | 'community', index: number) {
      if (section === 'hole') {
        this.hole[index] = null;
      } else {
        this.community[index] = null;
      }
    },

    async runAnalysis() {
      const activeHole = this.hole.filter((c): c is string => c !== null);
      const activeComm = this.community.filter((c): c is string => c !== null);
      
      if (activeHole.length < 2) return;
      
      this.loading = true;
      this.error = null;
      try {
        const response = await pokerApi.analyze({
          hole: activeHole,
          community: activeComm,
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
      } finally {
        this.loading = false;
      }
    },

    async resolveHand(outcome: 'win' | 'loss' | 'fold' | 'tie', chips?: number) {
      if (!this.roundId) return;
      
      try {
        await pokerApi.resolve(this.roundId, outcome, chips);
        this.clearHand();
      } catch (error: any) {
        this.error = error.response?.data?.error || error.message;
      }
    },

    clearHand() {
      this.hole = [null, null];
      this.community = [null, null, null, null, null];
      this.result = null;
      this.roundId = null;
    }
  }
});
