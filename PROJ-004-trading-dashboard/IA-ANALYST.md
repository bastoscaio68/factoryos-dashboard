# IA-ANALYST.md
# Documentação do Módulo IA Analyst
# PROJ-004 Trading Dashboard - GATE 3

## 1. Visão Geral

O módulo **IA Analyst** é a engine de análise de mercado e geração de recomendações do Trading Dashboard. Ele identifica o regime de mercado atual, classifica volatilidade e força do trend, e gera recomendações de trading otimizadas para cada perfil.

### Localização
```
docs/projetos/PROJ-004-trading-dashboard/src/services/ia_analyst.py
```

### Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                    IA ANALYST ENGINE                         │
├─────────────────────────────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐   │
│  │   Regime     │  │ Volatility   │  │   Trend Strength │   │
│  │  Analyzer    │  │  Classifier  │  │     Detector     │   │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘   │
│         │                 │                   │              │
│         └─────────────────┼───────────────────┘              │
│                           ▼                                  │
│              ┌─────────────────────────┐                    │
│              │    Market Analysis      │                    │
│              │    Dataclass             │                    │
│              └────────────┬────────────┘                    │
│                           ▼                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Profile Recommender                      │   │
│  │  (Seleciona melhor bot baseado no regime atual)       │   │
│  └──────────────────────┬──────────────────────────────┘   │
│                          ▼                                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │            Trading Recommendation                    │   │
│  │  • Tipo de bot     • Direção                         │   │
│  │  • Entry/TP/SL     • Alavancagem                     │   │
│  │  • Thesis          • Confiança                       │   │
│  └─────────────────────────────────────────────────────┘   │
│                           ▼                                  │
│              ┌─────────────────────────┐                    │
│              │   Signal for Risk       │                    │
│              │      Manager            │                    │
│              └─────────────────────────┘                    │
└─────────────────────────────────────────────────────────────┘
```

## 2. Componentes Principais

### 2.1 Enum: MarketRegime
Identifica o regime atual do mercado.

```python
class MarketRegime(Enum):
    BULL = "bull"       # Tendência de alta
    BEAR = "bear"       # Tendência de baixa
    SIDEWAYS = "sideways"  # Consolidação
    UNKNOWN = "unknown"
```

### 2.2 Enum: VolatilityLevel
Classifica a volatilidade baseada em ATR%.

```python
class VolatilityLevel(Enum):
    HIGH = "alta"       # ATR > 4%
    MEDIUM = "media"    # ATR 2-4%
    LOW = "baixa"       # ATR < 2%
    UNKNOWN = "unknown"
```

### 2.3 Enum: TrendStrength
Força do trend baseada em ADX.

```python
class TrendStrength(Enum):
    STRONG = "forte"      # ADX >= 25
    MODERATE = "moderado" # ADX 20-25
    WEAK = "fraco"        # ADX < 20
    UNKNOWN = "unknown"
```

### 2.4 Dataclass: MarketAnalysis
Resultado da análise de mercado.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `regime` | MarketRegime | Regime identificado |
| `volatility` | VolatilityLevel | Nível de volatilidade |
| `trend_strength` | TrendStrength | Força do trend |
| `adx_value` | float | Valor do ADX (0-100) |
| `atr_percent` | float | ATR como % do preço |
| `ema_20_position` | float | Preço vs EMA20 (%) |
| `rsi` | float | RSI (14) |
| `volume_regime` | float | Volume atual vs média |

### 2.5 Dataclass: TradingRecommendation
Recomendação gerada para o risk_manager.

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `signal_id` | str | ID único do sinal |
| `asset` | str | Par de trading |
| `bot_type` | BotType | Tipo recomendado |
| `direction` | TradingDirection | long/short/neutro |
| `entry_zone` | str | Zona de entrada sugerida |
| `take_profit_1` | str | Primeiro alvo |
| `take_profit_2` | str | Segundo alvo |
| `stop_loss` | str | Stop loss |
| `leverage` | float | Alavancagem ótima |
| `risk_reward_ratio` | float | R:R sugerido |
| `confidence_score` | float | 0-100 |
| `operational_range` | str | Faixa operacional |
| `thesis` | str | Tese de trading |
| `catalysts` | list[str] | Catalisadores |
| `risks` | list[str] | Riscos |

## 3. Performance por Perfil

### Base de Conhecimento (Scores por Regime)

| Perfil | Bull | Bear | Sideways |
|--------|------|------|----------|
| **Scalper** | 0.45 | 0.55 | 0.75 |
| **Day Trader** | 0.55 | 0.40 | 0.65 |
| **Swing Trader** | 0.75 | 0.35 | 0.45 |
| **Position Trader** | 0.80 | 0.45 | 0.30 |

### Win Rates Históricos

| Perfil | Bull | Bear | Sideways |
|--------|------|------|----------|
| **Scalper** | 42% | 48% | 58% |
| **Day Trader** | 50% | 42% | 55% |
| **Swing Trader** | 55% | 38% | 48% |
| **Position Trader** | 60% | 40% | 42% |

### Risk:Reward Médio

| Perfil | Bull | Bear | Sideways |
|--------|------|------|----------|
| **Scalper** | 1.2 | 1.3 | 1.4 |
| **Day Trader** | 1.5 | 1.4 | 1.6 |
| **Swing Trader** | 2.0 | 1.8 | 1.9 |
| **Position Trader** | 3.0 | 2.5 | 2.8 |

## 4. Algoritmos

### 4.1 Identificação de Regime

O algoritmo utiliza múltiplos indicadores:

1. **Posição do Preço vs EMAs**
   - Preço > EMA20 > EMA50 > EMA200 = Bull
   - Preço < EMA20 < EMA50 < EMA200 = Bear
   - Outro = Sideways

2. **RSI**
   - RSI 50-70 = Bullish
   - RSI 30-50 = Bearish
   - RSI < 30 = Oversold
   - RSI > 70 = Overbought

3. **Score de Decisão**
   - Bull Score >= 4 e Bear Score <= 2 → BULL
   - Bear Score >= 4 e Bull Score <= 2 → BEAR
   - Diferença <= 1 → SIDEWAYS

### 4.2 Classificação de Volatilidade

```python
if atr_percent > 4.0:
    return VolatilityLevel.HIGH
elif atr_percent >= 2.0:
    return VolatilityLevel.MEDIUM
else:
    return VolatilityLevel.LOW
```

### 4.3 Cálculo de ADX

```python
# +DI = (Soma +DM14 / ATR14) * 100
# -DI = (Soma -DM14 / ATR14) * 100
# DX = |+DI - -DI| / (+DI + -DI) * 100
# ADX = Média móvel simples de DX
```

### 4.4 Seleção de Perfil

Score Final = Regime × Volatilidade × Trend

```python
# Exemplo: Bull + Alta Vol + Trend Forte
Score = 0.80 × 1.2 (Scalper) × 1.1 (Swing) = 1.056
```

## 5. Uso da API

### 5.1 Análise de Regime

```python
from ia_analyst import analyze_market_regime

candles = [
    {"t": 1234567890, "o": 50000, "h": 50200, "l": 49800, "c": 50100, "v": 1000},
    # ... mais candles
]

analysis = analyze_market_regime(candles)
print(analysis)
# {
#     "regime": "bull",
#     "volatility": "media",
#     "trend_strength": "forte",
#     "adx_value": 28.5,
#     "atr_percent": 2.8,
#     ...
# }
```

### 5.2 Geração de Recomendação

```python
from ia_analyst import get_recommendation

result = get_recommendation(
    candles=candles,
    asset="BTC/USDT",
    current_price=50100
)

print(result["recommendation"])
# {
#     "sinal_id": "SIG-BTCUSDT-202402121200",
#     "ativo": "BTC/USDT",
#     "direcao": "long",
#     "entrada_zona": "$49500 ± $500",
#     "alvo_1": "$51000",
#     "alvo_2": "$52500",
#     "stop_loss": "$48500",
#     "risco_recompensa": "1:2.0",
#     "conviccao": "alta (70-80%)",
#     "tese": "Recomendação de compra...",
#     ...
# }
```

### 5.3 Consulta de Melhor Perfil

```python
from ia_analyst import get_best_profile_for_regime

result = get_best_profile_for_regime("bull")
print(result)
# {
#     "regime": "bull",
#     "recommended_profile": "position_trader",
#     "scores": {...}
# }
```

## 6. Formato de Sinal (Output)

O output segue o padrão definido em AGENTS.md:

```yaml
sinal_id: "SIG-BTCUSDT-202402121200"
ativo: "BTC/USDT"
direcao: "long"
timeframe: "4h"
entrada_zona: "$49500 ± $500"
alvo_1: "$51000"
alvo_2: "$52500"
stop_loss: "$48500"
risco_recompensa: "1:2.0"
conviccao: "alta (70-80%)"
tese: "Recomendação de compra baseada em tendência de alta..."
catalisadores:
  - Preço acima de médias móveis-chave
  - Momentum positivo
riscos_da_tese:
  - Reversão após overbought
  - Notícias negativas
validade_sinal: "24h"
fontes:
  - ia_analyst_engine
```

## 7. Integração com Outros Módulos

```
┌─────────────────────────────────────────────────────────────┐
│                      FLUXO COMPLETO                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  market_monitor ──► ia_analyst ──► risk_manager            │
│        │                                │                   │
│        │                         ┌──────┴──────┐             │
│        │                         │             │             │
│        │                    [APROVADO]     [VETADO]          │
│        │                         │             │             │
│        │                         ▼             ▼             │
│        │                    trading      analyst log        │
│        │                    trader                          │
│        │                                                  │
│  scraper (on-chain) ───────► ia_analyst                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## 8. Limitações e Considerações

### 8.1 Requisitos Mínimos
- Mínimo de 20 candles para análise
- Recomendado: 100+ candles para análise confiável

### 8.2 Limitações
- Análise baseada apenas em price action
- Não considera eventos macroeconômicos (deve ser complementado pelo market_monitor)
- Base de conhecimento atualizada periodicamente

### 8.3 Melhorias Futuras
- [ ] Machine Learning para ajuste dinâmico de pesos
- [ ] Integração com dados on-chain (Glassnode, CryptoQuant)
- [ ] Análise de sentimento (Fear & Greed Index)
- [ ] Backtesting automatizado

## 9. Testes

### Teste Automático

```bash
python src/services/ia_analyst.py
```

Expected output:
```
=== IA Analyst Test ===
Regime: bull
Volatilidade: media
Trend: forte

Recomendação:
  Bot: swing_trader
  Direção: long
  Confiança: alta (70-80%)
  Alavancagem: 1:2.0
```

## 10. Changelog

| Versão | Data | Descrição |
|--------|------|-----------|
| 1.0.0 | 2024-02-12 | Versão inicial (GATE 3) |

---

**Documento gerado em:** 2024-02-12  
**Responsável:** IA Analyst Engine (GATE 3)  
**Projeto:** PROJ-004 Trading Dashboard
