# PROJECT REQUEST EXTENSION — PROJ-003-EXT

> Extensão do PROJ-003 — File Browser para Dashboard
> Gate 1 Obrigatório.

---

## IDENTIFICAÇÃO

| Campo | Valor |
|-------|-------|
| ID Original | PROJ-003 |
| ID Extensão | PROJ-003-EXT |
| Nome | File Browser — Navegação e Download |
| Data | 2026-02-12 |
| Solicitante | Humano (Caio Bastos) |
| Tier | ENTERPRISE |

---

## OBJETIVO

Adicionar funcionalidade de **navegação de arquivos** ao Dashboard FactoryOS, permitindo:
- Visualizar estrutura de pastas
- Baixar arquivos diretamente
- Acessar artefatos de projetos

---

## ESCOPO

### Incluso

1. **API de Arquivos**
   - `GET /api/arquivos` → Lista pasta
   - `GET /api/arquivos/:path` → Download
   - Suporte a ícones por tipo (.html, .md, .js, etc.)

2. **Interface File Browser**
   - Nova aba "Arquivos" no Dashboard
   - Tree view de pastas
   - Ícones por tipo de arquivo
   - Botão download em cada arquivo
   - Breadcrumb de navegação

### Excluído

- Preview de arquivos (v2.0)
- Upload de arquivos (v2.0)
- Edição inline (v3.0)

---

## ENTREGÁVEIS

| # | Entregável | Descrição |
|---|------------|-----------|
| 1 | `api/files.js` | Endpoints de arquivos |
| 2 | `DASHBOARD.html` (atualizado) | Nova aba Arquivos |
| 3 | QA-REPORT.md | QA da extensão |

---

## PRAZO

| Marco | Data |
|-------|------|
| Início | 2026-02-12 07:25 |
| Entrega | 2026-02-12 07:35 |

---

## ARQUITETURA

### Endpoints

```
GET /api/arquivos
   ?path=docs/projetos
   → JSON: { folders: [...], files: [...] }

GET /api/arquivos/:path
   → Content-Disposition: attachment
```

### Interface

```
┌─────────────────────────────────────┐
│ [Projetos] [📁 Arquivos] [Manual]  │
├─────────────────────────────────────┤
│ 📁 docs/                            │
│ ├── 📁 projetos/                     │
│ │   ├── 📁 PROJ-001/                │
│ │   │   ├── 📄 SLIDES-001.html ⬇   │
│ │   │   └── 📄 REQUEST.md ⬇        │
│ │   ├── 📁 PROJ-002/                │
│ │   └── 📁 PROJ-003/                │
│ └── 📁 COMPANY/                     │
└─────────────────────────────────────┘
```

---

## APROVAÇÃO

| Campo | Valor |
|-------|-------|
| Aprovado por | Humano (Caio Bastos) |
| Data | 2026-02-12 07:25 |
| Status | ⏳ Aguardando |
