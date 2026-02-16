import React from 'react';
import { TradingProvider } from './context/TradingContext';
import Header from './components/Header';
import PerformanceCards from './components/PerformanceCards';
import PnLChart from './components/PnLChart';
import TradesTable from './components/TradesTable';
import AIRecommendation from './components/AIRecommendation';
import NewTradeModal from './components/NewTradeModal';
import './styles/App.css';

function App() {
  return (
    <TradingProvider>
      <div className="app">
        <Header />
        <main className="main-content">
          <PerformanceCards />
          <div className="charts-section">
            <PnLChart />
            <AIRecommendation />
          </div>
          <TradesTable />
        </main>
        <NewTradeModal />
      </div>
    </TradingProvider>
  );
}

export default App;
