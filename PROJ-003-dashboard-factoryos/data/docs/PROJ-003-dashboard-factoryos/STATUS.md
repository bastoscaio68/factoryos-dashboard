---
projeto_id: PROJ-003
nome: FactoryOS Dashboard — Plataforma de Gestão Visual
tier: ENTERPRISE
fase: Gate 3 (QA Final)
status: gate2_em_progresso
ultima_atualizacao: 2026-02-12 07:12
atualizado_por: orquestrador
---

## 📍 Estado Atual

**Gate atual:** 🟡 **GATE 3 — QA FINAL EM PROGRESSO**
**Status:** Aguardando quality_auditor
**Gate 1:** ✅ 07:12
**Gate 2:** ✅ 07:19
**Próximo:** Deploy no Vercel após QA aprovado

---

## 🎯 Objetivo do Projeto

Criar plataforma web para:
- ✅ Visualizar projetos em tempo real
- ✅ Criar novos projetos via interface
- ✅ Editar status de projetos
- ✅ Acessar de qualquer lugar (Vercel)
- ✅ Design moderno e responsivo

---

## 📂 Artefatos

| Artefato | Status | Descrição |
|---|---|---|
| REQUEST_PROJ-003.md | ✅ Gate 1 | Request do projeto |
| RESPONSIBILITY_MATRIX.md | ✅ | Matriz de fases |
| DESIGN-SYSTEM.md | ✅ brand_system | Cores, tipografia, componentes |
| api/server.js | ✅ scope_parser | API endpoints |
| deploy.sh | ✅ scope_parser | Script de deploy |
| DASHBOARD.html | ✅ presentation_builder | Interface principal |
| MANUAL.html | ✅ ideation | Manual completo em HTML |
| **QA-REPORT.md** | ⏳ **AGUARDANDO** | QA Final |

---

## 💬 Handoffs

**GATE 2 COMPLETO!**
- ✅ DESIGN-SYSTEM.md (brand_system)
- ✅ api/server.js (scope_parser)
- ✅ deploy.sh (scope_parser)
- ✅ DASHBOARD.html (presentation_builder)
- ✅ MANUAL.html (ideation)

**GATE 3 — QA Final:**
- ⏳ quality_auditor → QA-REPORT.md

---

## 🎨 Especificações do Design System

### Cores FactoryOS

| Cor | Hex | Uso |
|-----|-----|-----|
| Deep Ocean | #0a1628 | Background |
| Electric Blue | #00d4ff | Primary |
| Neon Cyan | #00ffcc | Accent |
| Surface 1 | rgba(10,22,40,0.9) | Cards |
| Surface 2 | rgba(10,22,40,0.6) | Secondary |

### Tipografia

| Fonte | Uso | Weight |
|-------|-----|--------|
| Inter | Corpo | 400, 500, 600, 700 |
| JetBrains Mono | Código | 400, 500 |

---

## 🔧 Especificações da API

### Endpoints

| Método | Rota | Descrição |
|--------|------|-----------|
| GET | /api/projetos | Lista todos os projetos |
| GET | /api/projetos/:id | Detalhes de um projeto |
| POST | /api/projetos | Cria novo projeto |
| PUT | /api/projetos/:id/status | Atualiza status |

---

## 📱 Responsividade

| Breakpoint | Layout |
|------------|--------|
| Desktop (>768px) | Grid 2-3 cards por linha |
| Tablet (768px) | Grid 2 cards por linha |
| Mobile (<768px) | 1 card por linha, full width |

---

## 🚀 Deploy

| Plataforma | URL | Status |
|------------|-----|--------|
| Vercel | factoryos-dashboard.vercel.app | ⏳ Pending |
| Custom | dashboard.factoryos.com | ⏳ Opcional |

---

## 📊 KSFs

| KSF | Status | Métrica |
|-----|--------|---------|
| KSF 1 | 🔄 | URL pública funcionando |
| KSF 2 | 🔄 | Tempo real (< 30s) |
| KSF 3 | ⏳ | Formulário cria projetos |
| KSF 4 | ⏳ | Todos dados visíveis |
| KSF 5 | ⏳ | Mobile + Desktop |

---

## 💬 Handoffs Pendentes

[Aguardando Gate 2 completar → ideation cria MANUAL.html]
