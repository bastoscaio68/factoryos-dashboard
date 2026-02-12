# PROJECT REQUEST — PROJ-003

> Gate 1 obrigatório para projetos ENTERPRISE.
> Sem este documento aprovado pelo humano, o projeto não inicia.

---

## IDENTIFICAÇÃO

| Campo | Valor |
|-------|-------|
| ID do Projeto | PROJ-003 |
| Nome | FactoryOS Dashboard — Plataforma de Gestão Visual |
| Data da Request | 2026-02-12 |
| Solicitante | Humano (Caio Bastos) |
| Tier | 🔴 ENTERPRISE |
| Departamento Principal | INTERNAL (Operações) |
| Orquestrador responsável | orquestrador |

---

## OBJETIVO DO PROJETO

Criar uma **plataforma web de gestão visual** para o FactoryOS Multi-Agentes IA, permitindo:

### Funcionalidades Principais

| Funcionalidade | Descrição | Prioridade |
|----------------|-----------|------------|
| **Visualização** | Cards de projetos em tempo real | 🔴 Alta |
| **Status Tracking** | Acompanhar progresso de cada projeto | 🔴 Alta |
| **Criação de Projetos** | Formulário para iniciar novos projetos | 🔴 Alta |
| **Edição de Status** | Atualizar status via interface | 🟡 Média |
| **Detalhes Completos** | Ver KSFs, artefatos, timeline | 🟡 Média |
| **Acesso Remoto** | Publicar na internet (Vercel) | 🔴 Alta |
| **Tempo Real** | WebSocket ou polling automático | 🔴 Alta |

### Público-Alvo

| Persona | Necessidade |
|---------|-------------|
| **Caio Bastos** | Visualizar projetos, criar novos, acompanhar progresso |
| **Equipe** | Ver status, atualizar progresso (futuro) |
| **Clientes** | Visualizar progresso de projetos (futuro) |

---

## ESCOPO

### Incluso

- **Dashboard Web**
  - Interface moderna e responsiva (mobile-first)
  - Cards de projetos com informações completas
  - Filtros por status (todos/ativos/aguardando/concluídos)
  - Stats agregados (contagem por status)
  - Auto-refresh configurável

- **Criação de Projetos**
  - Formulário completo (nome, tier, departamento, objetivo, prazo)
  - Validação de dados
  - Criação automática de estrutura de pastas

- **Edição de Status**
  - Interface para alterar status de projetos
  - Registro automático no PDCA_LOG

- **Publicação**
  - Deploy automático no Vercel
  - Custom domain opcional
  - SSL automático

### Excluído

- Autenticação de usuários (v1.0)
- Múltiplos usuários (v1.0)
- Notificações push (v2.0)
- Relatórios avançados (v2.0)

### Premissas

- Projeto focado no uso do Caio (single-user inicialmente)
- Dashboard lê dados do servidor via API
- Sistema de gates mantido (aprovação humana obrigatória)

---

## ENTREGÁVEIS ESPERADOS

| # | Entregável | Formato | Descrição |
|---|------------|---------|-----------|
| 1 | DASHBOARD.html | HTML/CSS/JS | Interface principal |
| 2 | API Endpoint | Node.js/Python | `/api/projetos` retorna JSON |
| 3 | API Endpoint | Node.js/Python | `/api/projetos/:id` detalha projeto |
| 4 | API Endpoint | Node.js/Python | POST `/api/projetos` cria projeto |
| 5 | API Endpoint | Node.js/Python | PUT `/api/projetos/:id/status` edita status |
| 6 | Manual.html | HTML | Manual de uso e instalação |
| 7 | Deploy Script | Shell | Script de deploy no Vercel |
| 8 | README.md | Markdown | Documentação técnica |

---

## PRAZO

| Marco | Data | Descrição |
|-------|------|-----------|
| Início | 2026-02-12 | Aprovação do Gate 1 |
| Entrega v1.0 | 2026-02-12 | Dashboard completo |
| Deploy Produção | 2026-02-12 | No ar em vercel.app |

---

## BUDGET

| Campo | Valor |
|-------|-------|
| Custo de hospedagem | US$ 0 (Vercel free tier) |
| Domínio customizado | US$ 12/ano (opcional) |
| Estimativa de horas | 4-6 horas |

---

## ARQUITETURA

### Frontend

```
DASHBOARD.html
├── HTML5 semântico
├── CSS3 (CSS Grid, Flexbox, Custom Properties)
├── JavaScript ES6+ (vanilla, sem frameworks)
└── Design System FactoryOS (cores, tipografia)
```

### Backend (API)

```
/api/projetos
├── GET /projetos          → Lista todos
├── GET /projetos/:id     → Detalhes
├── POST /projetos         → Cria
├── PUT /projetos/:id/status → Edita status
└── WebSocket (futuro)    → Tempo real
```

### Integração

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  DASHBOARD  │◄──►│     API     │◄──►│  Arquivos   │
│   (Vercel)   │     │ (OpenClaw) │     │  .md        │
└─────────────┘     └─────────────┘     └─────────────┘
```

---

## RISCOS IDENTIFICADOS

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| CORS bloqueando API | Média | Alto | Configurar headers corretos |
| WebSocket complex demais | Alta | Médio | Usar polling primeiro |
| Deploy falhar | Baixa | Alto | Script com retry |
| Dados não sincronizam | Média | Alto | Refresh manual disponível |

---

## CRITÉRIOS DE SUCESSO (KSFs)

| KSF | Descrição | Métrica |
|-----|-----------|----------|
| KSF 1 | Dashboard acessível remotamente | URL pública funcionando |
| KSF 2 | Tempo real | Dados atualizam em < 30s |
| KSF 3 | Criação de projetos | Formulário cria estrutura completa |
| KSF 4 | Visualização completa | Todos os dados visíveis |
| KSF 5 | Design responsivo | Funciona mobile e desktop |

---

## APROVAÇÃO

| Campo | Valor |
|-------|-------|
| Aprovado por | Humano (Caio Bastos) |
| Data | 2026-02-12 |
| Status | ⏳ Aguardando aprovação |

---

> **Após aprovação:** Orquestrador cria estrutura de pastas e inicia execução.
