# Trading Dashboard Backend

Backend API para Trading Dashboard com análise de mercado, detecção de regimes e recomendações de setup.

## Estrutura do Projeto

```
src/
├── api/
│   ├── v1/
│   │   ├── auth.py
│   │   ├── trades.py
│   │   ├── portfolio.py
│   │   ├── analysis.py
│   │   └── market.py
│   └── websocket/
│       └── manager.py
├── core/
│   ├── config.py
│   ├── security.py
│   └── database.py
├── models/
│   ├── user.py
│   ├── trade.py
│   ├── performance_metric.py
│   ├── market_regime.py
│   └── portfolio_history.py
├── services/
│   ├── coinGecko_client.py
│   ├── regime_detection.py
│   └── setup_recommendation.py
├── schemas/
│   ├── auth.py
│   ├── trade.py
│   └── ...
└── main.py
```

## Requisitos

- Python 3.11+
- PostgreSQL 15+
- Redis 7+

## Instalação

```bash
pip install -r requirements.txt
```

## Executar

```bash
uvicorn src.main:app --reload
```

## API Documentation

Acesse `http://localhost:8000/docs` para ver a documentação Swagger.
