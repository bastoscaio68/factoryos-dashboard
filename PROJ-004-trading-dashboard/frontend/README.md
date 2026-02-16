# Trading Dashboard Frontend

## PROJ-004 - Trading Dashboard

Dashboard React para monitoramento de trades e performance de trading.

## 📋 Visão Geral

Frontend desenvolvido em React para visualização de dados de trading, incluindo:
- Métricas em tempo real (saldo, PnL, preço BTC)
- Gráfico de PnL acumulado
- Tabela de trades com filtros e ordenação
- Cards de performance (Win Rate, Profit Factor, Sharpe Ratio, Max Drawdown)
- Painel de recomendações via IA
- Modal para registro de novos trades

## 🛠️ Tecnologias

- **React 18**
- **Chart.js** / react-chartjs-2
- **Axios** para requisições HTTP
- **date-fns** para manipulação de datas
- **Lucide React** para ícones
- **CSS3** com variáveis CSS

## 📁 Estrutura

```
frontend/
├── public/
│   └── index.html
├── src/
│   ├── api/
│   │   └── api.js              # Configuração da API
│   ├── components/
│   │   ├── Header.js           # Header com métricas
│   │   ├── PerformanceCards.js # Cards de performance
│   │   ├── PnLChart.js         # Gráfico de PnL
│   │   ├── TradesTable.js      # Tabela de trades
│   │   ├── AIRecommendation.js # Painel IA
│   │   └── NewTradeModal.js    # Modal de novo trade
│   ├── context/
│   │   └── TradingContext.js   # Estado global
│   ├── styles/
│   │   ├── index.css           # Estilos globais
│   │   ├── App.css
│   │   ├── Header.css
│   │   ├── PerformanceCards.css
│   │   ├── PnLChart.css
│   │   ├── TradesTable.css
│   │   ├── AIRecommendation.css
│   │   └── NewTradeModal.css
│   ├── App.js
│   └── index.js
├── package.json
└── README.md
```

## 🚀 Instalação

```bash
# Navegar para o diretório
cd frontend

# Instalar dependências
npm install

# Criar arquivo de variáveis de ambiente
cp .env.example .env

# Iniciar desenvolvimento
npm start
```

## ⚙️ Configuração

Crie um arquivo `.env` na raiz do frontend:

```env
REACT_APP_API_URL=http://localhost:8000/api
```

## 📡 Integração com Backend

O frontend se conecta à API REST em `http://localhost:8000/api`:

| Endpoint | Método | Descrição |
|----------|--------|-----------|
| `/balance` | GET | Saldo atual |
| `/pnl` | GET | PnL (daily, weekly, monthly, total) |
| `/btc/price` | GET | Preço do Bitcoin |
| `/trades` | GET/POST | Lista/Criação de trades |
| `/performance` | GET | Métricas de performance |
| `/ai/recommendation` | GET | Recomendações IA |

## 🎨 Features

### Header
- Exibição de saldo total
- PnL diário com cores condicionais
- Preço BTC/USDT em tempo real
- Botão para novo trade

### Gráfico de PnL
- Período selecionável (7d, 30d, 90d)
- Visualização acumulada
- Tooltips informativos

### Tabela de Trades
- Ordenação por colunas
- Filtros por status (Win/Loss/Breakeven)
- Busca por símbolo
- Status visual (badges coloridos)

### Performance Cards
- Win Rate
- Profit Factor
- Sharpe Ratio
- Max Drawdown

### IA Recommendations
- Recomendação de ação (BUY/SELL/HOLD)
- Nível de confiança
- Nível de risco
- Análise descritiva

### Novo Trade Modal
- Seleção de símbolo
- Side (Long/Short)
- Preços de entrada/saída
- Quantidade
- Stop Loss / Take Profit
- Notas

## 🔄 Atualização de Dados

Os dados são atualizados automaticamente a cada 30 segundos via polling no `TradingContext`.

```javascript
// No TradingContext.js
useEffect(() => {
  fetchData();
  const interval = setInterval(fetchData, 30000);
  return () => clearInterval(interval);
}, [fetchData]);
```

## 📱 Responsividade

O dashboard é totalmente responsivo:
- Desktop: Layout completo com sidebar
- Tablet: Grid adaptativo
- Mobile: Componentes empilhados

## 🎯 Próximos Passos

- [ ] Adicionar autenticação
- [ ] Implementar WebSocket para dados em tempo real
- [ ] Adicionar mais indicadores técnicos
- [ ] Implementar tema dark/light
- [ ] Adicionar testes unitários

## 📄 Licença

Este projeto é parte do PROJ-004 - Trading Dashboard.
