import React, { useState, useEffect } from 'react';
import { useTrading } from '../context/TradingContext';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js';
import { Line } from 'react-chartjs-2';
import '../styles/PnLChart.css';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
);

const PnLChart = () => {
  const { pnl } = useTrading();
  const [period, setPeriod] = useState('7d');

  const generateChartData = (period) => {
    const days = period === '7d' ? 7 : period === '30d' ? 30 : 90;
    const labels = [];
    const data = [];

    let currentPnl = pnl.monthly * 0.3;

    for (let i = days; i >= 0; i--) {
      const date = new Date();
      date.setDate(date.getDate() - i);
      labels.push(date.toLocaleDateString('pt-BR', { day: '2-digit', month: '2-digit' }));

      const dailyChange = (Math.random() - 0.45) * 500;
      currentPnl += dailyChange;
      data.push(currentPnl);
    }

    return { labels, data };
  };

  const { labels, data } = generateChartData(period);

  const chartData = {
    labels,
    datasets: [
      {
        label: 'PnL Acumulado',
        data,
        borderColor: '#22c55e',
        backgroundColor: (context) => {
          const ctx = context.chart.ctx;
          const gradient = ctx.createLinearGradient(0, 0, 0, 300);
          gradient.addColorStop(0, 'rgba(34, 197, 94, 0.3)');
          gradient.addColorStop(1, 'rgba(34, 197, 94, 0)');
          return gradient;
        },
        fill: true,
        tension: 0.4,
        pointRadius: 2,
        pointHoverRadius: 6,
        pointHoverBackgroundColor: '#22c55e',
        pointHoverBorderColor: '#fff',
        pointHoverBorderWidth: 2
      }
    ]
  };

  const chartOptions = {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: {
        display: false
      },
      tooltip: {
        backgroundColor: '#1f2937',
        titleColor: '#fff',
        bodyColor: '#fff',
        padding: 12,
        displayColors: false,
        callbacks: {
          label: (context) => {
            const value = context.parsed.y;
            return `PnL: ${value >= 0 ? '+' : ''}$${value.toFixed(2)}`;
          }
        }
      }
    },
    scales: {
      x: {
        grid: {
          display: false
        },
        ticks: {
          color: '#9ca3af',
          maxTicksLimit: 7
        }
      },
      y: {
        grid: {
          color: 'rgba(156, 163, 175, 0.1)'
        },
        ticks: {
          color: '#9ca3af',
          callback: (value) => `$${value}`
        }
      }
    },
    interaction: {
      intersect: false,
      mode: 'index'
    }
  };

  return (
    <div className="pnl-chart-container">
      <div className="chart-header">
        <h3>PnL Acumulado</h3>
        <div className="chart-period-selector">
          {['7d', '30d', '90d'].map((p) => (
            <button
              key={p}
              className={`period-btn ${period === p ? 'active' : ''}`}
              onClick={() => setPeriod(p)}
            >
              {p.toUpperCase()}
            </button>
          ))}
        </div>
      </div>
      <div className="chart-wrapper">
        <Line data={chartData} options={chartOptions} />
      </div>
    </div>
  );
};

export default PnLChart;
