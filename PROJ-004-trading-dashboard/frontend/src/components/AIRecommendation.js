import React from 'react';
import { useTrading } from '../context/TradingContext';
import { Sparkles, ArrowUp, ArrowDown, Minus, AlertTriangle } from 'lucide-react';
import '../styles/AIRecommendation.css';

const AIRecommendation = () => {
  const { aiRecommendation } = useTrading();

  if (!aiRecommendation) {
    return (
      <div className="ai-recommendation-container">
        <div className="ai-header">
          <Sparkles size={20} />
          <h3>IA Recommendation</h3>
        </div>
        <div className="ai-loading">Carregando recomendações...</div>
      </div>
    );
  }

  const getActionIcon = (action) => {
    switch (action) {
      case 'BUY': return <ArrowUp size={24} />;
      case 'SELL': return <ArrowDown size={24} />;
      default: return <Minus size={24} />;
    }
  };

  const getActionClass = (action) => {
    return `action-${action.toLowerCase()}`;
  };

  const getRiskClass = (risk) => {
    switch (risk) {
      case 'LOW': return 'risk-low';
      case 'MEDIUM': return 'risk-medium';
      case 'HIGH': return 'risk-high';
      default: return '';
    }
  };

  const getRiskLabel = (risk) => {
    switch (risk) {
      case 'LOW': return 'Risco Baixo';
      case 'MEDIUM': return 'Risco Médio';
      case 'HIGH': return 'Risco Alto';
      default: return risk;
    }
  };

  return (
    <div className="ai-recommendation-container">
      <div className="ai-header">
        <Sparkles size={20} />
        <h3>IA Recommendation</h3>
      </div>

      <div className="ai-content">
        <div className="recommendation-main">
          <div className={`action-badge ${getActionClass(aiRecommendation.action)}`}>
            {getActionIcon(aiRecommendation.action)}
            <span>{aiRecommendation.action}</span>
          </div>
          <div className="symbol-info">
            <span className="symbol">{aiRecommendation.symbol}</span>
            <div className={`risk-badge ${getRiskClass(aiRecommendation.riskLevel)}`}>
              <AlertTriangle size={14} />
              {getRiskLabel(aiRecommendation.riskLevel)}
            </div>
          </div>
        </div>

        <div className="confidence-section">
          <span className="confidence-label">Confiança</span>
          <div className="confidence-bar">
            <div
              className="confidence-fill"
              style={{ width: `${aiRecommendation.confidence}%` }}
            />
          </div>
          <span className="confidence-value">{aiRecommendation.confidence}%</span>
        </div>

        <div className="reason-section">
          <span className="reason-label">Análise</span>
          <p className="reason-text">{aiRecommendation.reason}</p>
        </div>

        <div className="ai-footer">
          <span className="disclaimer">
            ⚠️ Esta é uma recomendação gerada por IA. Always DYOR.
          </span>
        </div>
      </div>
    </div>
  );
};

export default AIRecommendation;
