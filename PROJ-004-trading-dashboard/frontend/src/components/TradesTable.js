import React, { useState } from 'react';
import { useTrading } from '../context/TradingContext';
import { Search, Filter, ChevronDown, ChevronUp, ExternalLink } from 'lucide-react';
import '../styles/TradesTable.css';

const TradesTable = () => {
  const { trades } = useTrading();
  const [sortField, setSortField] = useState('timestamp');
  const [sortDirection, setSortDirection] = useState('desc');
  const [filter, setFilter] = useState('all');
  const [searchTerm, setSearchTerm] = useState('');

  const filteredTrades = trades.filter(trade => {
    const matchesSearch = trade.symbol.toLowerCase().includes(searchTerm.toLowerCase());
    const matchesFilter = filter === 'all' || trade.status === filter;
    return matchesSearch && matchesFilter;
  });

  const sortedTrades = [...filteredTrades].sort((a, b) => {
    let aVal = a[sortField];
    let bVal = b[sortField];

    if (typeof aVal === 'string') {
      aVal = aVal.toLowerCase();
      bVal = bVal.toLowerCase();
    }

    if (sortDirection === 'asc') {
      return aVal > bVal ? 1 : -1;
    }
    return aVal < bVal ? 1 : -1;
  });

  const handleSort = (field) => {
    if (sortField === field) {
      setSortDirection(sortDirection === 'asc' ? 'desc' : 'asc');
    } else {
      setSortField(field);
      setSortDirection('desc');
    }
  };

  const formatDate = (timestamp) => {
    return new Date(timestamp).toLocaleString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const getStatusBadge = (status) => {
    const classes = {
      win: 'badge-win',
      loss: 'badge-loss',
      breakeven: 'badge-breakeven'
    };
    const labels = {
      win: 'Win',
      loss: 'Loss',
      breakeven: 'Breakeven'
    };
    return <span className={`badge ${classes[status]}`}>{labels[status]}</span>;
  };

  const getSideBadge = (side) => {
    return <span className={`badge badge-${side}`}>{side.toUpperCase()}</span>;
  };

  return (
    <div className="trades-table-container">
      <div className="table-header">
        <h3>Histórico de Trades</h3>
        <div className="table-controls">
          <div className="search-box">
            <Search size={18} />
            <input
              type="text"
              placeholder="Buscar símbolo..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
            />
          </div>
          <div className="filter-box">
            <Filter size={18} />
            <select value={filter} onChange={(e) => setFilter(e.target.value)}>
              <option value="all">Todos</option>
              <option value="win">Wins</option>
              <option value="loss">Losses</option>
              <option value="breakeven">Breakeven</option>
            </select>
          </div>
        </div>
      </div>

      <div className="table-wrapper">
        <table className="trades-table">
          <thead>
            <tr>
              <th onClick={() => handleSort('timestamp')}>
                Data/Hora
                {sortField === 'timestamp' && (
                  sortDirection === 'asc' ? <ChevronUp size={14} /> : <ChevronDown size={14} />
                )}
              </th>
              <th onClick={() => handleSort('symbol')}>
                Símbolo
                {sortField === 'symbol' && (
                  sortDirection === 'asc' ? <ChevronUp size={14} /> : <ChevronDown size={14} />
                )}
              </th>
              <th onClick={() => handleSort('side')}>
                Side
                {sortField === 'side' && (
                  sortDirection === 'asc' ? <ChevronUp size={14} /> : <ChevronDown size={14} />
                )}
              </th>
              <th onClick={() => handleSort('entryPrice')}>
                Entry
                {sortField === 'entryPrice' && (
                  sortDirection === 'asc' ? <ChevronUp size={14} /> : <ChevronDown size={14} />
                )}
              </th>
              <th onClick={() => handleSort('exitPrice')}>
                Exit
                {sortField === 'exitPrice' && (
                  sortDirection === 'asc' ? <ChevronUp size={14} /> : <ChevronDown size={14} />
                )}
              </th>
              <th onClick={() => handleSort('quantity')}>
                Qtd
                {sortField === 'quantity' && (
                  sortDirection === 'asc' ? <ChevronUp size={14} /> : <ChevronDown size={14} />
                )}
              </th>
              <th onClick={() => handleSort('pnl')}>
                PnL
                {sortField === 'pnl' && (
                  sortDirection === 'asc' ? <ChevronUp size={14} /> : <ChevronDown size={14} />
                )}
              </th>
              <th onClick={() => handleSort('status')}>
                Status
                {sortField === 'status' && (
                  sortDirection === 'asc' ? <ChevronUp size={14} /> : <ChevronDown size={14} />
                )}
              </th>
              <th>Duração</th>
            </tr>
          </thead>
          <tbody>
            {sortedTrades.length > 0 ? (
              sortedTrades.map((trade) => (
                <tr key={trade.id}>
                  <td className="timestamp-cell">{formatDate(trade.timestamp)}</td>
                  <td className="symbol-cell">{trade.symbol}</td>
                  <td>{getSideBadge(trade.side)}</td>
                  <td>${trade.entryPrice.toFixed(2)}</td>
                  <td>${trade.exitPrice.toFixed(2)}</td>
                  <td>{trade.quantity.toFixed(4)}</td>
                  <td className={`pnl-cell ${trade.pnl >= 0 ? 'positive' : 'negative'}`}>
                    {trade.pnl >= 0 ? '+' : ''}${trade.pnl.toFixed(2)}
                    <span className="pnl-percent">
                      ({trade.pnlPercent >= 0 ? '+' : ''}{trade.pnlPercent.toFixed(2)}%)
                    </span>
                  </td>
                  <td>{getStatusBadge(trade.status)}</td>
                  <td className="duration-cell">{trade.duration}h</td>
                </tr>
              ))
            ) : (
              <tr>
                <td colSpan="9" className="no-data">
                  Nenhum trade encontrado
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default TradesTable;
