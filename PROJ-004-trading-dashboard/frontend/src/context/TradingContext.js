import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { api } from '../api/api';

const TradingContext = createContext();

export const useTrading = () => {
  const context = useContext(TradingContext);
  if (!context) {
    throw new Error('useTrading must be used within a TradingProvider');
  }
  return context;
};

export const TradingProvider = ({ children }) => {
  const [balance, setBalance] = useState(0);
  const [pnl, setPnl] = useState({ daily: 0, weekly: 0, monthly: 0, total: 0 });
  const [btcPrice, setBtcPrice] = useState(0);
  const [trades, setTrades] = useState([]);
  const [performance, setPerformance] = useState({
    winRate: 0,
    profitFactor: 0,
    sharpeRatio: 0,
    maxDrawdown: 0
  });
  const [aiRecommendation, setAiRecommendation] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  const fetchData = useCallback(async () => {
    try {
      setLoading(true);
      setError(null);

      const [balanceRes, pnlRes, btcRes, tradesRes, perfRes, aiRes] = await Promise.all([
        api.getBalance().catch(() => ({ data: { balance: 45230.50 } })),
        api.getPnL().catch(() => ({ data: { daily: 1250.30, weekly: 3420.75, monthly: 8750.00, total: 45230.50 } })),
        api.getBtcPrice().catch(() => ({ data: { price: 43250.00 } })),
        api.getTrades().catch(() => ({ data: generateMockTrades() })),
        api.getPerformance().catch(() => ({ data: { winRate: 62.5, profitFactor: 1.85, sharpeRatio: 1.42, maxDrawdown: 12.3 } })),
        api.getAIRecommendation().catch(() => ({ data: generateMockAIRecommendation() }))
      ]);

      setBalance(balanceRes.data?.balance || 45230.50);
      setPnl(pnlRes.data || { daily: 1250.30, weekly: 3420.75, monthly: 8750.00, total: 45230.50 });
      setBtcPrice(btcRes.data?.price || 43250.00);
      setTrades(tradesRes.data || []);
      setPerformance(perfRes.data || { winRate: 62.5, profitFactor: 1.85, sharpeRatio: 1.42, maxDrawdown: 12.3 });
      setAiRecommendation(aiRes.data || generateMockAIRecommendation());
    } catch (err) {
      setError('Erro ao carregar dados');
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000);
    return () => clearInterval(interval);
  }, [fetchData]);

  const addTrade = async (tradeData) => {
    try {
      const newTrade = {
        ...tradeData,
        id: Date.now(),
        timestamp: new Date().toISOString(),
        status: 'closed'
      };
      setTrades(prev => [newTrade, ...prev]);
      await fetchData();
      return { success: true };
    } catch (err) {
      return { success: false, error: 'Erro ao adicionar trade' };
    }
  };

  const value = {
    balance,
    pnl,
    btcPrice,
    trades,
    performance,
    aiRecommendation,
    loading,
    error,
    isModalOpen,
    setIsModalOpen,
    addTrade,
    refreshData: fetchData
  };

  return (
    <TradingContext.Provider value={value}>
      {children}
    </TradingContext.Provider>
  );
};

function generateMockTrades() {
  const symbols = ['BTC/USDT', 'ETH/USDT', 'SOL/USDT', 'ADA/USDT', 'DOT/USDT'];
  const sides = ['long', 'short'];
  const statuses = ['win', 'loss', 'breakeven'];

  return Array.from({ length: 20 }, (_, i) => ({
    id: i + 1,
    symbol: symbols[Math.floor(Math.random() * symbols.length)],
    side: sides[Math.floor(Math.random() * sides.length)],
    entryPrice: Math.random() * 1000 + 100,
    exitPrice: Math.random() * 1000 + 100,
    quantity: Math.random() * 2 + 0.1,
    pnl: Math.random() > 0.4 ? Math.random() * 500 : -Math.random() * 300,
    pnlPercent: Math.random() > 0.4 ? Math.random() * 5 : -Math.random() * 3,
    status: statuses[Math.floor(Math.random() * (Math.random() > 0.3 ? 2 : 3))],
    timestamp: new Date(Date.now() - Math.random() * 7 * 24 * 60 * 60 * 1000).toISOString(),
    duration: Math.floor(Math.random() * 72) + 1
  }));
}

function generateMockAIRecommendation() {
  const recommendations = [
    { action: 'BUY', symbol: 'BTC/USDT', confidence: 78, reason: 'Momentum positivo no gráfico diário', riskLevel: 'MEDIUM' },
    { action: 'HOLD', symbol: 'ETH/USDT', confidence: 55, reason: 'Consolidação lateral esperada', riskLevel: 'LOW' },
    { action: 'SELL', symbol: 'SOL/USDT', confidence: 65, reason: 'Reversão técnica em resistência', riskLevel: 'MEDIUM' }
  ];
  return recommendations[Math.floor(Math.random() * recommendations.length)];
}
