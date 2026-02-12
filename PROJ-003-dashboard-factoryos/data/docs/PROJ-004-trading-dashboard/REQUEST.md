# PROJ-004 — Trading Dashboard Quantitativo

> **Status:** PLANEJAMENTO
> **Gate:** Gate 0 — Validação Inicial
> **Criado:** 2026-02-12
> **Prioridade:** 🔴 ALTA (Estratégico)

---

## 📋 Requisição de Projeto

**Objetivo:** Desenvolver um Dashboard Inteligente de Trading Quantitativo para BTC

### Problema que resolve:
- Falta de controle estruturado de performance
- Decisão emocional em regime de mercado
- Dificuldade de identificar qual perfil performa melhor
- Falta de padronização nas entradas
- Ausência de recomendação quantitativa baseada em histórico

### Resultados esperados:
- ✅ Dashboard analítico completo
- ✅ Análise histórica por perfil (grid, trend alta, trend baixa, etc)
- ✅ Sistema de recomendação baseado em regime de mercado
- ✅ Geração automática de parâmetros de bot
- ✅ Redução de erro operacional
- ✅ Evolução progressiva da assertividade

### Público-alvo:
- Trader quantitativo individual
- Operador de bots Pionex Futures
- Usuário focado em BTC
- Perfil técnico e orientado a dados

---

## 🎯 Escopo Técnico

### Formato do Output:
- **HTML (Web App Responsivo)** com backend
- Interface web moderna (dark mode tech/futurista)
- Backend com banco de dados persistente
- Gráficos dinâmicos

### Ferramentas Autorizadas:
- ✅ ChatGPT (motor analítico IA)
- ✅ Python (backend + lógica quantitativa)
- ✅ FastAPI ou Flask
- ✅ React ou Next.js
- ✅ Chart.js ou TradingView Lightweight Charts
- ✅ PostgreSQL ou SQLite
- ✅ Integração API de dados BTC (Binance ou CoinGecko)
- ❌ Midjourney / DALL-E (não necessário)

### Regras Específicas:

**Sistema deve armazenar:**
- Data do trade
- Perfil do trade
- Resultado (% e USDT)
- Alavancagem
- Setup utilizado
- Entrada, TP, SL

**Perfis iniciais:**
- Grid
- Trend Alta
- Trend Baixa
- Lateralização
- Breakout

**IA Analista deve:**
- Identificar regime atual do BTC
- Avaliar qual perfil historicamente performa melhor nesse regime
- Indicar:
  - Tipo de bot
  - Direção
  - Entrada, TP, SL
  - Faixa operacional
  - Alavancagem sugerida

---

## ✅ Critérios de Sucesso

### MVP Obrigatório:
- [ ] Registro de trades funcional
- [ ] Controle de aportes e retiradas
- [ ] Dashboard com:
  - PnL acumulado
  - Curva de capital
  - Performance por perfil
- [ ] Script /trade funcionando
- [ ] Recomendação automática de setup

### Excelência:
- [ ] Análise histórica cruzada com regime de mercado
- [ ] Sistema evolutivo (aprende com histórico)
- [ ] Interface moderna estilo fintech
- [ ] Métricas avançadas
- [ ] Diagnóstico crítico da operação

---

## 📅 Cronograma Sugerido

| Fase | Duração | Entregável |
|------|---------|------------|
| Gate 0: Validação | 1 dia | Escopo aprovado |
| Gate 1: Estrutura | 3 dias | Backend + DB + API |
| Gate 2: Frontend | 5 dias | Dashboard + Gráficos |
| Gate 3: IA Analyst | 4 dias | Sistema de recomendação |
| Gate 4: Integração | 2 dias | Script /trade + Testes |
| Gate 5: QA | 2 dias | Validação completa |
| **Total** | **~17 dias** | **MVP Completo** |

---

*Criado por: Caio Bastos*
*Data: 2026-02-12*
