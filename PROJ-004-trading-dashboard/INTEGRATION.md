# GATE 4 — Integração (PROJ-004 Trading Dashboard)

**Projeto:** PROJ-004-trading-dashboard  
**Data:** 2024-01-15  
**Status:** ✅ Concluído

## 1. Visão Geral da Integração

Este documento descreve a integração completa do sistema Trading Dashboard, conectando:
- **Backend**: FastAPI (porta 3000)
- **Frontend**: React/Vite (porta 3001)
- **Banco de Dados**: PostgreSQL (porta 5432)
- **Cache**: Redis (porta 6379)

## 2. Estrutura do Projeto

```
PROJ-004-trading-dashboard/
├── src/                      # Backend FastAPI
│   ├── main.py              # Entry point da API
│   ├── config.py            # Configurações
│   ├── models/              # Modelos SQLAlchemy
│   │   ├── database.py
│   │   └── trade.py
│   ├── schemas/             # Schemas Pydantic
│   │   └── trade.py
│   ├── routers/             # Endpoints da API
│   │   ├── trades.py
│   │   └── analytics.py
│   └── services/             # Lógica de negócio
│       └── analytics.py
├── frontend/                  # Frontend React
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Dashboard.jsx
│   │   │   ├── Trades.jsx
│   │   │   ├── Analytics.jsx
│   │   │   └── NewTrade.jsx
│   │   ├── services/
│   │   │   └── api.js
│   │   └── App.jsx
│   ├── package.json
│   └── vite.config.js
├── scripts/
│   └── trade.py             # CLI de registro
├── docker-compose.yml       # Orquestração
├── Dockerfile.backend       # imagem Docker
├── requirements.txt         # Dependências Python
└── setup.sh                # Script de setup/deploy
```

## 3. Endpoints da API

### 3.1 Trades

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| POST | `/api/trades` | Criar novo trade |
| GET | `/api/trades` | Listar trades |
| GET | `/api/trades/{id}` | Detalhar trade |
| PUT | `/api/trades/{id}` | Atualizar trade |
| DELETE | `/api/trades/{id}` | Deletar trade |

### 3.2 Analytics

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/api/analytics` | Métricas agregadas |
| GET | `/api/recommendation` | Recomendação IA |

### 3.3 Health Check

| Método | Endpoint | Descrição |
|--------|----------|-----------|
| GET | `/` | Info da API |
| GET | `/health` | Health check |

## 4. Configuração CORS

O CORS está configurado no FastAPI para permitir todas as origens em desenvolvimento:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, limitar origens
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 5. URLs de API no Frontend

O frontend está configurado para conectar ao backend via proxy Vite (desenvolvimento) ou URL completa (produção):

```javascript
// frontend/src/services/api.js
const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3000/api'
```

### Configuração de Produção

Para produção, defina a variável de ambiente:
```bash
VITE_API_URL=https://api.seudominio.com/api
```

## 6. Script de Deploy

### 6.1 Instalação

```bash
cd docs/projetos/PROJ-004-trading-dashboard
./setup.sh install
```

### 6.2 Iniciar com Docker

```bash
# Iniciar todos os serviços
./setup.sh docker-up

# Ver logs
./setup.sh docker-logs

# Parar serviços
./setup.sh docker-down
```

### 6.3 Desenvolvimento Local

```bash
# Iniciar apenas o backend
./setup.sh start-backend

# Iniciar apenas o frontend
./setup.sh start-frontend

# Iniciar ambos
./setup.sh start-all
```

## 7. Teste End-to-End

### 7.1 Registrar Trade via CLI

```bash
cd docs/projetos/PROJ-004-trading-dashboard
python scripts/trade.py --interactive
```

Exemplo de entrada:
```
Data/Hora [2024-01-15T14:30:00]: 
Perfil: trend_alta
Resultado (%): 2.5
Resultado (USDT): 125.0
Alavancagem (1-125): 10
Setup: scalp_5m
Entrada: 43250.50
Take Profit (TP): 43500.00
Stop Loss (SL): 43000.00
```

### 7.2 Visualizar no Dashboard

1. Acesse `http://localhost:3001`
2. Veja métricas na página inicial
3. Navegue para "Trades" para ver lista completa
4. Use "+ Novo Trade" para registro manual

### 7.3 IA Recommendation

A recomendação IA está disponível em:
- **Dashboard**: Card de recomendação na página inicial
- **API**: `GET /api/recommendation`

Exemplo de resposta:
```json
{
  "recommendation": "Continue operando no perfil 'trend_alta' com setup 'scalp_5m'. Win rate de 65.2%",
  "confidence": 85,
  "based_on": {
    "total_trades": 25,
    "best_profile": "trend_alta",
    "best_profile_win_rate": 65.2,
    "best_setup": "scalp_5m",
    "best_setup_pnl": 450.0
  }
}
```

## 8. Variáveis de Ambiente

### Backend

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| DATABASE_URL | postgresql://... | String de conexão PostgreSQL |
| REDIS_URL | redis://... | URL do Redis |
| API_TOKEN | dev-token-12345 | Token de autenticação |
| API_PORT | 3000 | Porta da API |

### Frontend

| Variável | Padrão | Descrição |
|----------|--------|-----------|
| VITE_API_URL | http://localhost:3000/api | URL da API |

## 9. Testes de Integração

### 9.1 Teste de Criação de Trade

```bash
./setup.sh test-api
```

Este comando:
1. Envia um trade de teste para a API
2. Verifica a resposta
3. Testa endpoints de analytics
4. Testa recomendação IA

### 9.2 Teste Manual com cURL

```bash
# Health check
curl http://localhost:3000/health

# Criar trade
curl -X POST http://localhost:3000/api/trades \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer dev-token-12345" \
  -d '{
    "datetime": "2024-01-15T14:30:00",
    "profile": "trend_alta",
    "setup": "scalp_5m",
    "pair": "BTC/USDT",
    "entry": 43250.50,
    "tp": 43500.00,
    "sl": 43000.00,
    "result_percent": 2.5,
    "result_usdt": 125.0,
    "leverage": 10
  }'

# Listar trades
curl http://localhost:3000/api/trades \
  -H "Authorization: Bearer dev-token-12345"

# Analytics
curl http://localhost:3000/api/analytics \
  -H "Authorization: Bearer dev-token-12345"
```

## 10. Troubleshooting

### 10.1 Erro de Conexão com Banco

```
sqlalchemy.excrete.OperationalError: could not connect to server
```

**Solução**: Verificar se o PostgreSQL está rodando:
```bash
docker-compose ps
docker-compose logs postgres
```

### 10.2 CORS Erro no Frontend

```
Access to fetch at 'http://localhost:3000/api/trades' from origin 'http://localhost:3001' has been blocked by CORS policy
```

**Solução**: Verificar configuração CORS em `src/main.py`

### 10.3 Token Inválido

```
{"detail": "Unauthorized"}
```

**Solução**: Verificar se o token no frontend (`src/services/api.js`) corresponde ao `API_TOKEN` nas variáveis de ambiente

## 11. Próximos Passos (GATE 5+)

- [ ] Integração com API da Binance
- [ ] Integração com API da Bybit  
- [ ] Autenticação JWT completa
- [ ] Deploy em produção (Vercel + Railway)
- [ ] Testes automatizados (Pytest + Jest)

## 12. Arquitetura de Integração

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   Frontend      │────▶│   Backend API     │────▶│   PostgreSQL    │
│   (React :3001) │     │   (FastAPI:3000) │     │   (Postgres)    │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                               │
                               ▼
                        ┌──────────────────┐
                        │   Redis Cache    │
                        │   (Redis)        │
                        └──────────────────┘
```

---

**Status**: ✅ Pronto para QA  
**Responsável**: [Bot Manager Agent]  
**Data**: 2024-01-15
