import React, { useState } from 'react';
import { useTrading } from '../context/TradingContext';
import { X, TrendingUp, TrendingDown } from 'lucide-react';
import '../styles/NewTradeModal.css';

const NewTradeModal = () => {
  const { isModalOpen, setIsModalOpen, addTrade } = useTrading();
  const [formData, setFormData] = useState({
    symbol: 'BTC/USDT',
    side: 'long',
    entryPrice: '',
    exitPrice: '',
    quantity: '',
    stopLoss: '',
    takeProfit: '',
    notes: ''
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const tradeData = {
        ...formData,
        entryPrice: parseFloat(formData.entryPrice),
        exitPrice: parseFloat(formData.exitPrice),
        quantity: parseFloat(formData.quantity),
        stopLoss: formData.stopLoss ? parseFloat(formData.stopLoss) : null,
        takeProfit: formData.takeProfit ? parseFloat(formData.takeProfit) : null
      };

      const result = await addTrade(tradeData);
      if (result.success) {
        setIsModalOpen(false);
        setFormData({
          symbol: 'BTC/USDT',
          side: 'long',
          entryPrice: '',
          exitPrice: '',
          quantity: '',
          stopLoss: '',
          takeProfit: '',
          notes: ''
        });
      } else {
        setError(result.error);
      }
    } catch (err) {
      setError('Erro ao salvar trade. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  const handleClose = () => {
    setIsModalOpen(false);
    setError('');
  };

  if (!isModalOpen) return null;

  return (
    <div className="modal-overlay" onClick={handleClose}>
      <div className="modal-content" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <h2>Novo Trade</h2>
          <button className="close-btn" onClick={handleClose}>
            <X size={24} />
          </button>
        </div>

        <form onSubmit={handleSubmit} className="trade-form">
          {error && <div className="error-message">{error}</div>}

          <div className="form-row">
            <div className="form-group">
              <label>Símbolo</label>
              <select name="symbol" value={formData.symbol} onChange={handleChange}>
                <option value="BTC/USDT">BTC/USDT</option>
                <option value="ETH/USDT">ETH/USDT</option>
                <option value="SOL/USDT">SOL/USDT</option>
                <option value="ADA/USDT">ADA/USDT</option>
                <option value="DOT/USDT">DOT/USDT</option>
              </select>
            </div>

            <div className="form-group">
              <label>Side</label>
              <div className="side-selector">
                <button
                  type="button"
                  className={`side-btn ${formData.side === 'long' ? 'active-long' : ''}`}
                  onClick={() => setFormData({ ...formData, side: 'long' })}
                >
                  <TrendingUp size={16} />
                  Long
                </button>
                <button
                  type="button"
                  className={`side-btn ${formData.side === 'short' ? 'active-short' : ''}`}
                  onClick={() => setFormData({ ...formData, side: 'short' })}
                >
                  <TrendingDown size={16} />
                  Short
                </button>
              </div>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Preço de Entrada</label>
              <input
                type="number"
                name="entryPrice"
                value={formData.entryPrice}
                onChange={handleChange}
                step="0.01"
                placeholder="0.00"
                required
              />
            </div>

            <div className="form-group">
              <label>Preço de Saída</label>
              <input
                type="number"
                name="exitPrice"
                value={formData.exitPrice}
                onChange={handleChange}
                step="0.01"
                placeholder="0.00"
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label>Quantidade</label>
              <input
                type="number"
                name="quantity"
                value={formData.quantity}
                onChange={handleChange}
                step="0.0001"
                placeholder="0.0000"
                required
              />
            </div>

            <div className="form-group">
              <label>Stop Loss (opcional)</label>
              <input
                type="number"
                name="stopLoss"
                value={formData.stopLoss}
                onChange={handleChange}
                step="0.01"
                placeholder="0.00"
              />
            </div>

            <div className="form-group">
              <label>Take Profit (opcional)</label>
              <input
                type="number"
                name="takeProfit"
                value={formData.takeProfit}
                onChange={handleChange}
                step="0.01"
                placeholder="0.00"
              />
            </div>
          </div>

          <div className="form-group">
            <label>Notas (opcional)</label>
            <textarea
              name="notes"
              value={formData.notes}
              onChange={handleChange}
              placeholder="Adicione observações sobre o trade..."
              rows="3"
            />
          </div>

          <div className="form-actions">
            <button type="button" className="btn-cancel" onClick={handleClose}>
              Cancelar
            </button>
            <button type="submit" className="btn-submit" disabled={loading}>
              {loading ? 'Salvando...' : 'Salvar Trade'}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};

export default NewTradeModal;
