import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

export const api = {
  // Balance
  getBalance: () => apiClient.get('/balance'),

  // PnL
  getPnL: (period = 'all') => apiClient.get(`/pnl?period=${period}`),
  getPnLHistory: (days = 30) => apiClient.get(`/pnl/history?days=${days}`),

  // Bitcoin Price
  getBtcPrice: () => apiClient.get('/btc/price'),

  // Trades
  getTrades: (filters = {}) => {
    const params = new URLSearchParams(filters);
    return apiClient.get(`/trades?${params}`);
  },
  createTrade: (data) => apiClient.post('/trades', data),
  updateTrade: (id, data) => apiClient.put(`/trades/${id}`, data),
  deleteTrade: (id) => apiClient.delete(`/trades/${id}`),

  // Performance
  getPerformance: () => apiClient.get('/performance'),

  // AI Recommendations
  getAIRecommendation: () => apiClient.get('/ai/recommendation'),

  // Market Data
  getMarketData: (symbol) => apiClient.get(`/market/${symbol}`)
};

export default api;
