import React from 'react';
import { useTrading } from '../context/TradingContext';
import { Target, BarChart3, TrendingDown, Activity } from 'lucide-react';
import '../styles/PerformanceCards.css';

const PerformanceCards = () => {
  const { performance } = useTrading();

  const cards = [
    {
      title: 'Win Rate',
      value: `${performance.winRate}%`,
      icon: Target,
      color: '#22c55e'
    },
    {
      title: 'Profit Factor',
      value: performance.profitFactor.toFixed(2),
      icon: BarChart3,
      color: '#3b82f6'
    },
    {
      title: 'Sharpe Ratio',
      value: performance.sharpeRatio.toFixed(2),
      icon: Activity,
      color: '#8b5cf6'
    },
    {
      title: 'Max Drawdown',
      value: `-${performance.maxDrawdown}%`,
      icon: TrendingDown,
      color: '#ef4444'
    }
  ];

  return (
    <div className="performance-cards">
      {cards.map((card, index) => (
        <div key={index} className="perf-card">
          <div className="perf-card-header">
            <card.icon size={20} style={{ color: card.color }} />
            <span className="perf-title">{card.title}</span>
          </div>
          <span className="perf-value">{card.value}</span>
        </div>
      ))}
    </div>
  );
};

export default PerformanceCards;
