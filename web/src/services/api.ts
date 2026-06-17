import axios from 'axios';

// Dynamically determine API URL based on the current window location
const API_IP = window.location.hostname;
const api = axios.create({
  baseURL: `http://${API_IP}:5000/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add a response interceptor for better debugging
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export interface PokerAnalyzeRequest {
  hole: string[];
  community?: string[];
  opponents?: number;
  aggression?: number[];
  record?: boolean;
  round_id?: string;
  session_id?: string;
}

export interface PokerAnalyzeResponse {
  win_rate: number;
  tie_rate: number;
  loss_rate: number;
  hand_name: string;
  recommendation: string;
  equity_iterations: number;
  metadata?: {
    round_id?: string;
  };
}

export const pokerApi = {
  analyze: (data: PokerAnalyzeRequest) => 
    api.post<PokerAnalyzeResponse>('/poker/analyze', data).then(r => r.data),
  
  resolve: (id: string, outcome: string, chips?: number) =>
    api.post('/history/resolve', { id, outcome, chips }).then(r => r.data),
};

export default api;
