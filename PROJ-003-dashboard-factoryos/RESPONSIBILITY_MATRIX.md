# RESPONSIBILITY MATRIX — PROJ-003

> Gate 3 — obrigatório para ENTERPRISE.
> Fonte da verdade para dependências e sequência de execução.

---

## RESUMO DO PROJETO

| Campo | Valor |
|-------|-------|
| Projeto | PROJ-003 — FactoryOS Dashboard |
| Tier | ENTERPRISE |
| Fase atual | Planejamento |
| Última atualização | 2026-02-12 07:12 |

---

## MATRIZ DE FASES E ENTREGÁVEIS

| # | Fase / Entregável | Agente Owner | Input Necessário | Output / Artefato | Prazo | Status | Observações |
|---|---|---|---|---|---|---|---|
| 01 | Design System | brand_system | Manual de marca | DESIGN-SYSTEM.md | D+0 | ✅ | |
| 02 | API Backend | scope_parser | DESIGN-SYSTEM.md | api/server.js | D+0 | ✅ | |
| 03 | Dashboard Frontend | presentation_builder | DESIGN-SYSTEM.md | DASHBOARD.html | D+0 | ✅ | |
| 04 | Manual HTML | ideation | Todos acima | MANUAL.html | D+0 | ✅ | |
| 05 | Script Deploy | scope_parser | API + Dashboard | deploy.sh | D+0 | ✅ | |
| 06 | QA Final | quality_auditor | Todos artefatos | QA-REPORT.md | D+0 | ✅ | |

---

## DEPENDÊNCIAS CRÍTICAS

```
brand_system ──────► presentation_builder ──► QA
        │                              │
        └────────► scope_parser ───────┘
                     │
                     ▼
               ideation ─► MANUAL.html
                     │
                     ▼
               deploy.sh ──► QA
```

---

## ARQUITETURA DETALHADA

### Frontend (presentation_builder)

```
DASHBOARD.html
├── Header (logo + stats)
├── Tabs (filtros)
├── Projects Grid (cards)
│   ├── Card (projeto individual)
│   │   ├── ID + Name
│   │   ├── Tier badge
│   │   ├── Status badge
│   │   ├── Gate progress
│   │   ├── KSFs
│   │   ├── Artefatos
│   │   └── Actions (view/edit)
│   └── Modal (novo/edição)
├── Footer (last updated)
└── Refresh Button (flutuante)
```

### Backend (scope_parser)

```
api/server.js
├── GET /projetos
│   └── Lê INDEX.md → JSON
├── GET /projetos/:id
│   └── Lê STATUS.md → JSON
├── POST /projetos
│   └── Cria estrutura de pastas
├── PUT /projetos/:id/status
│   └── Atualiza STATUS.md
│   └── Append PDCA_LOG.md
└── WebSocket (futuro)
    └── Emit events em tempo real
```

---

## AGENTES ATIVOS NESTE PROJETO

| Agente | Função no Projeto | Fases | Status |
|---|---|---|---|
| orquestrador | Coordenação geral | Todas | ⏳ |
| brand_system | Design System | 01 | ⏳ |
| scope_parser | API + Deploy Script | 02, 05 | ⏳ |
| presentation_builder | Dashboard Frontend | 03 | ⏳ |
| ideation | Manual HTML | 04 | ⏳ |
| quality_auditor | QA Final | 06 | ⏳ |

---

## AGENTES EM STANDBY

| Agente | Condição de Ativação |
|---|---|
| brain | Para validação estratégica do design |
| crypto_analyst | Para integração de market data (futuro) |

---

## LOG DE MUDANÇAS DE ESCOPO

[APPEND ONLY — registrar mudanças]

[2026-02-12] orquestrador: Projeto iniciado baseado no pedido do Caio para Dashboard em tempo real com publicação no Vercel | Impacto: Múltiplos entregáveis (API, HTML, Manual, Deploy)

---

## OBSERVAÇÕES

- Projeto ENTERPRISE requer QA antes de deploy
- API deve ser integrada ao OpenClaw gateway
- Dashboard deve funcionar offline (graceful degradation)
- Manual deve ser HTML apresentável
