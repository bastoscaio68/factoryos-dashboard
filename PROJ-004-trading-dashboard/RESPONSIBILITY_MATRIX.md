# RESPONSIBILITY MATRIX — PROJ-004

> **Projeto:** Trading Dashboard Quantitativo
> **Criado:** 2026-02-12

---

## 👥 Agents e Papéis

| Agent | Papel | Responsabilidade |
|-------|-------|------------------|
| **brain** | Arquiteto + Strategist | Arquitetura, estratégia, validação |
| **scope_parser** | Requisitos | Especificação técnica detalhada |
| **calc_engine** | Cálculos | Lógica quantitativa, métricas |
| **engineering/scope_parser** | Backend | API, banco de dados, Python |
| **engineering/drawing_generator** | Frontend | Dashboard, React/Next.js, Charts |
| **trading/crypto_analyst** | Domain Expert | Estratégia de trading, regimes BTC |
| **quality_auditor** | QA | Validação, testes, padrões |

---

## 🚦 Gates e Transições────────────────────────────────────────────────────────────────

```
┌─┐
│                        GATE 0 — VALIDAÇÃO                        │
│  brain analisa escopo → Aprova → scope_parser detalha           │
│  brain rejeita → Retorna para complementar                       │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                        GATE 1 — ESTRUTURA                       │
│  engineering/scope_parser → Backend API                           │
│  calc_engine → Lógica de métricas                               │
│  Dono: brain                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                        GATE 2 — FRONTEND                         │
│  engineering/drawing_generator → Dashboard React                   │
│  Charts → TradingView/Chart.js                                   │
│  Dono: brain                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                      GATE 3 — IA ANALYST                        │
│  trading/crypto_analyst → Análise de regime                     │
│  brain → Recomendação de setup                                  │
│  Dono: brain                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     GATE 4 — INTEGRAÇÃO                         │
│  Todos os agents → Conexão total                               │
│  Script /trade → Funcional                                     │
│  Dono: brain                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                        GATE 5 — QA                              │
│  quality_auditor → Auditoria final                               │
│  brain → Aprovação final                                        │
│  Stakeholder → Validação                                        │
└─────────────────────────────────────────────────────────────────┘
                              ↓
                          COMPLETO
```

---

## 📋 Entregas por Gate

| Gate | Entregável | Dono | Precisa de |
|------|------------|------|------------|
| Gate 0 | Escopo aprovado | brain | Caio |
| Gate 1 | API + DB + Models | scope_parser | calc_engine |
| Gate 2 | Dashboard Completo | drawing_generator | calc_engine |
| Gate 3 | IA Analyst | crypto_analyst | brain |
| Gate 4 | Sistema Integrado | todos | quality_auditor |
| Gate 5 | MVP Pronto | quality_auditor | Caio |

---

## 🔄 Critérios de Transição

| Gate → Gate | Critério |
|-------------|----------|
| 0 → 1 | Escopo aprovado + Tech stack definida |
| 1 → 2 | API funcional + DB populado |
| 2 → 3 | Dashboard visualizando dados |
| 3 → 4 | IA gerando recomendações |
| 4 → 5 | Sistema funcionando end-to-end |
| 5 → Concluído | QA aprovado + Stakeholder OK |

---

## ⚠️ Bloqueios Conhecidos

- Nenhum no momento

---

## 📞 Dependências

- Nenhuma dependência externa
