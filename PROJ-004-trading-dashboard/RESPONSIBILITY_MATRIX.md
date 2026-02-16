# RESPONSIBILITY MATRIX — PROJ-004

> **Projeto:** Trading Dashboard Quantitativo
> **Criado:** 2026-02-12

---

## 👥 Agents e Papéis

| Agent | Papel | Responsabilidade |
|-------|-------|------------------|
| **brain** | Arquiteto + Strategist | Arquitetura, estratégia, validação |
| **engineering/scope_parser** | Requisitos + Backend | Especificação técnica, API, DB, Python |
| **engineering/calc_engine** | Quant Engineer | Lógica quantitativa, métricas, PnL |
| **design/brand_system** | UX/UI Designer | Design gráfico, identidade visual, Charts |
| **ops/bot_manager** | DevOps | Script /trade, automações, integração |
| **trading/crypto_analyst** | Domain Expert | Estratégia de trading, regimes BTC |
| **quality_auditor** | QA | Validação, testes, padrões |

---

## 🚦 Gates e Transições

```
┌─────────────────────────────────────────────────────────────────┐
│                        GATE 0 — VALIDAÇÃO                       │
│  brain analisa escopo → Solicita aprovação humana               │
│  Humano aprova → engineering/scope_parser detalha               │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   GATE 1 — ESPECIFICAÇÃO + DESIGN               │
│  engineering/scope_parser → RD Técnica                          │
│  design/brand_system → Wireframes e Design System               │
│  calc_engine → Definição de métricas                            │
│  Dono: brain                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   GATE 2 — BACKEND + SCRIPTS                    │
│  engineering/scope_parser → API + DB + Models                   │
│  ops/bot_manager → Script /trade (automação)                    │
│  calc_engine → Lógica de PnL e métricas                         │
│  Dono: brain                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   GATE 3 — FRONTEND + IA                       │
│  design/brand_system → Dashboard React + Gráficos               │
│  trading/crypto_analyst → Análise de regime + recomendação     │
│  Dono: brain                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                   GATE 4 — INTEGRAÇÃO                           │
│  ops/bot_manager → Conexão script ↔ API                       │
│  todos → Testes end-to-end                                      │
│  Dono: brain                                                   │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                        GATE 5 — QA                              │
│  quality_auditor → Auditoria final                             │
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
| Gate 1 | RD Técnica + Design System | engineering/scope_parser + design/brand_system | calc_engine |
| Gate 2 | API + DB + Script /trade | engineering/scope_parser + ops/bot_manager | calc_engine |
| Gate 3 | Dashboard + IA Analyst | design/brand_system + trading/crypto_analyst | brain |
| Gate 4 | Sistema Integrado | ops/bot_manager + todos | quality_auditor |
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
