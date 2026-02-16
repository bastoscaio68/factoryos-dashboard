import React from 'react';
import { useTrading } from '../context/TradingContext';
import { Wallet, TrendingUp, Bitcoin, Plus } from 'lucide-react';
import '../styles/Header.css';

const Header = () => {
  const { balance, pnl, btcPrice, setIsModalOpen } = useTrading();

  const formatCurrency = (value) => {
    return new Intl.NumberFormat('pt-BR', {
      style: 'currency',
      currency: 'USD'
    }).format(value);
  };

  const formatBtcPrice = (value) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 2
    }).format(value);
  };

  const getPnLClass = (value) => {
    if (value > 0) return 'positive';
    if (value < 0) return 'negative';
    return '';
  };

  return (
    <header className="header">
      <div className="header-left">
        <div className="logo">
          <TrendingUp size={28} />
          <span>Trading Dashboard</span>
        </div>
      </div>

      <div className="header-metrics">
        <div className="metric-card">
          <div className="metric-icon wallet">
            <Wallet size={20} />
          </div>
          <div className="metric-info">
            <span className="metric-label">Saldo</span>
            <span className="metric-value">{formatCurrency(balance)}</span>
          </div>
        </div>

        <div className="metric-card">
          <div className={`metric-icon ${getPnLClass(pnl.daily)}`}>
            <TrendingUp size={20} />
          </div>
          <div className="metric-info">
            <span className="metric-label">PnL Diário</span>
            <span className={`metric-value ${getPnLClass(pnl.daily)}`}>
              {pnl.daily > 0 ? '+' : ''}{formatCurrency(pnl.daily)}
            </span>
          </div>
        </div>

        <div className="metric-card">
          <div className="metric-icon btc">
            <Bitcoin size={20} />
          </div>
          <div className="metric-info">
            <span className="metric-label">BTC/USDT</span>
            <span className="metric-value">{formatBtcPrice(btcPrice)}</span>
          </div>
        </div>

        <button className="btn-new-trade" onClick={() => setIsModalOpen(true)}>
          <Plus size={18} />
          Novo Trade
        </button>
      </div>
    </header>
  );
};

export default Header;
