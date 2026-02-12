# Manual do FactoryOS Dashboard

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Instalação](#instalação)
3. [Como Usar](#como-usar)
4. [Interpretação dos Dados](#interpretação-dos-dados)
5. [Funcionalidades](#funcionalidades)
6. [Limitações](#limitações)
7. [Solução de Problemas](#solução-de-problemas)
8. [Roadmap Futuro](#roadmap-futuro)
9. [Glossário](#glossário)

---

## Visão Geral

O **FactoryOS Dashboard** é uma interface web para visualizar e gerenciar projetos do sistema OpenClaw Multi-Agentes IA.

### O que ele faz

| Funcionalidade | Descrição |
|---------------|-----------|
| 📊 **Visualização** | Lista todos os projetos com status, tier, última atualização |
| 📈 **Métricas** | Contagem de projetos por status (ativos, aguardando, concluídos) |
| 🔍 **Filtros** | Abas para filtrar por status |
| 📱 **Mobile-first** | Funciona perfeitamente em celulares |
| 🔄 **Auto-refresh** | Atualiza automaticamente a cada 30 segundos |
| ➕ **Novo Projeto** | Formulário para criar novos projetos |
| ✏️ **Edição** | (Em desenvolvimento) Editar status de projetos |

### O que ele NÃO faz (ainda)

| Funcionalidade | Status |
|---------------|--------|
| Criar projetos reais | Em desenvolvimento |
| Editar status | Em desenvolvimento |
| WebSocket real-time | Planejado |
| Autenticação | Planejado |
| Múltiplos usuários | Planejado |

---

## Instalação

### Opção 1: Abrir diretamente (mais simples)

```bash
# Apenas abra o arquivo HTML no navegador:
file:///home/team/.openclaw/docs/projetos/DASHBOARD.html
```

**Vantagens:** Não precisa de servidor
**Desvantagens:** Algumas funcionalidades de JS podem não funcionar (CORS)

---

### Opção 2: Servidor HTTP local (recomendado)

```bash
# Navegue até a pasta de projetos
cd /home/team/.openclaw/docs/projetos

# Inicie um servidor Python (se instalado)
python3 -m http.server 8080

# Ou use npx serve (se instalado)
npx serve .

# Acesse no navegador
# http://localhost:8080/DASHBOARD.html
```

---

### Opção 3: Servidor OpenClaw

```bash
# Se o OpenClaw estiver rodando
# O dashboard já está disponível em:
# http://localhost:PORTA/docs/projetos/DASHBOARD.html
```

---

### Requisitos

| Requisito | Versão Mínima | Recomendado |
|-----------|---------------|--------------|
| Navegador | Chrome 80+ | Chrome 120+ |
| | Firefox 75+ | Firefox 120+ |
| | Safari 13+ | Safari 17+ |
| | Edge 80+ | Edge 120+ |
| JavaScript | ES6+ | ES2022 |
| Conexão | Não requerida | - |

---

## Como Usar

### 1. Abrir o Dashboard

```bash
# 1. Abra o terminal
# 2. Execute (se usando Python):
python3 -m http.server 8080 --directory /home/team/.openclaw/docs/projetos

# 3. No navegador, acesse:
http://localhost:8080/DASHBOARD.html
```

### 2. Visualizar Projetos

O dashboard abre automaticamente mostrando todos os projetos:

```
┌─────────────────────────────────────────┐
│  FactoryOS Dashboard                    │  ← Cabeçalho
├─────────────────────────────────────────┤
│  [+ Novo Projeto]                       │  ← Botão de ação
├─────────────────────────────────────────┤
│  ┌─────────┐ ┌─────────┐ ┌─────────┐  │  ← Stats
│  │    0    │ │    0    │ │    2    │  │
│  │Ativos   │ │Aguard.  │ │Concluíd.│  │
│  └─────────┘ └─────────┘ └─────────┘  │
├─────────────────────────────────────────┤
│  [Todos] [Ativos] [Aguardando] [Concluídos]  │  ← Abas de filtro
├─────────────────────────────────────────┤
│  ┌─────────────────────────────────────┐  │
│  │ PROJ-001                            │  │
│  │ Procedure Check + Marketing Visual  │  │  ← Card de projeto
│  │ ENTERPRISE | ✅ Concluído          │  │
│  │ [Ver Detalhes] [Editar]             │  │
│  └─────────────────────────────────────┘  │
│  ┌─────────────────────────────────────┐  │
│  │ PROJ-002                            │  │
│  │ Melhoria da Qualidade Visual         │  │
│  │ ENTERPRISE | ✅ Concluído          │  │
│  │ [Ver Detalhes]                      │  │
│  └─────────────────────────────────────┘  │
└─────────────────────────────────────────┘
```

### 3. Filtrar por Status

Clique nas abas para filtrar:

| Aba | Mostra |
|-----|--------|
| **Todos** | Todos os projetos |
| **Ativos** | Projetos em execução |
| **Aguardando** | Projetos parados, esperando decisão |
| **Concluídos** | Projetos finalizados |

### 4. Ver Detalhes de um Projeto

Clique em **"Ver Detalhes"** para ver informações completas.

### 5. Criar Novo Projeto

1. Clique no botão **"[+ Novo Projeto]"**
2. Preencha o formulário:
   - **Nome do Projeto** (obrigatório)
   - **Tier** (LITE / MEDIUM / ENTERPRISE)
   - **Departamento** (opcional)
   - **Objetivo** (obrigatório)
   - **Prazo** (opcional)
3. Clique em **"Criar Projeto"**

---

## Interpretação dos Dados

### Entendendo os Status

| Status | Significado | Ação Recomendada |
|--------|-------------|------------------|
| 🟢 **Em Andamento** | Projeto executando normalmente | Monitorar progresso |
| 🟡 **Aguardando Decisão** | Projeto parado, esperando humano | Revisar e aprovar/rejeitar |
| 🔴 **Bloqueado** | Projeto com problema crítico | Intervenção necessária |
| ✅ **Concluído** | Projeto finalizado | Arquivar |
| ⏸️ **Pausado** | Projeto intencionalmente parado | Revisar reason |

### Entendendo os Tiers

| Tier | Complexidade | Gates | Tempo Estimado |
|------|-------------|-------|----------------|
| 🟢 **LITE** | Simples | 1-2 | 1-4 horas |
| 🟡 **MEDIUM** | Média | 2-3 | 4-24 horas |
| 🔴 **ENTERPRISE** | Alta | 4-5+ | 24+ horas |

### Entendendo as Métricas

```
Stats = Contagem de projetos por status

Exemplo:
- 3 projetos ativos
- 2 aguardando decisão
- 5 concluídos
- Total: 10 projetos
```

---

## Funcionalidades

### ✅ Implementadas

#### Visualização de Projetos

Cada card de projeto mostra:

```
┌─────────────────────────────────────┐
│ PROJ-XXX                           │  ← ID do projeto
│ Nome Completo do Projeto            │  ← Título
│ ENTERPRISE | ✅ Concluído          │  ← Tier + Status
│ Ultima Atualização: DD/MM HH:MM    │  ← Timestamp
│ [Ver Detalhes] [Editar]           │  ← Ações
└─────────────────────────────────────┘
```

#### Sistema de Abas

| Aba | Descrição | CSS Class |
|-----|-----------|-----------|
| Todos | Mostra todos os projetos | `tab active` (quando selecionada) |
| Ativos | Filtra `status === 'ativo'` | - |
| Aguardando | Filtra `status === 'aguardando'` | - |
| Concluídos | Filtra `status === 'concluido'` | - |

#### Auto-Refresh

O dashboard atualiza automaticamente a cada **30 segundos**.

Para atualizar manualmente, clique no botão de refresh no canto inferior direito.

#### Design Mobile-First

O dashboard é **totalmente responsivo**:

| Tela | Layout |
|------|--------|
| Desktop (>768px) | Cards em grid, 2-3 por linha |
| Tablet (768px) | Cards em grid, 2 por linha |
| Mobile (<768px) | Cards empilhados, 1 por linha |

---

### ⚠️ Em Desenvolvimento

#### Criação de Projetos

O formulário está pronto, mas a integração com o OpenClaw não foi implementada.

**O que acontece quando você clica em "Criar Projeto":**
```
1. Formulário valida os campos
2. JS cria objeto do projeto
3. (?) Envia para API do OpenClaw
4. (?) Cria arquivos STATUS.md, PDCA_LOG.md
5. (?) Inicia workflow de gates
```

**Status atual:** Modal abre, mas não cria projetos ainda.

#### Edição de Status

**O que está planejado:**

```
1. Clique em "Editar"
2. Modal mostra status atual
3. Selecione novo status
4. Confirme a mudança
5. STATUS.md é atualizado
6. PDCA_LOG registra mudança
```

**Status atual:** Botão existe, mas não funciona ainda.

---

## Limitações

### Limitações Técnicas

| Limitação | Descrição | Solução Alternativa |
|-----------|-----------|-------------------|
| **Sem backend real** | JS só lê, não grava | Aguardar implementação |
| **Sem autenticação** | Qualquer um pode ver/editar | Usar em rede segura |
| **Sem persistência** | Dados perdidos ao fechar | Já estão nos arquivos MD |
| **Sem WebSocket** | Refresh só a cada 30s | Manual refresh |
| **CORS** | Arquivo local pode ter restrições | Usar servidor HTTP |

### Limitações de Funcionalidade

| Funcionalidade | Status | ETA |
|----------------|--------|-----|
| Criar projetos | Em desenvolvimento | v1.1 |
| Editar status | Em desenvolvimento | v1.1 |
| Ver detalhes | Parcial | v1.1 |
| Múltiplos usuários | Planejado | v2.0 |
| Notificações | Planejado | v2.0 |
| Relatórios | Planejado | v2.0 |

### Limitações de Dados

| Limitação | Descrição |
|-----------|-----------|
| **Dados mockados** | Por enquanto, lê de INDEX.md hardcoded |
| **Arquivos não integrados** | STATUS.md de cada projeto não está sendo lido |
| **Sem histórico** | PDCA_LOG não visualizado |

---

## Solução de Problemas

### Problema: Dashboard não carrega

**Sintoma:** Página em branco ou erro de carregamento

**Solução:**

```bash
# 1. Verifique se está usando servidor HTTP
# Python:
python3 -m http.server 8080

# 2. Verifique o console do navegador
# (F12 > Console)

# 3. Limpe o cache
# Ctrl+Shift+R (hard refresh)
```

---

### Problema: Projetos não aparecem

**Sintoma:** "Nenhum projeto encontrado" ou lista vazia

**Solução:**

```bash
# 1. Verifique se os projetos existem
ls -la /home/team/.openclaw/docs/projetos/

# 2. Verifique o INDEX.md
cat /home/team/.openclaw/docs/projetos/INDEX.md

# 3. Verifique formato do INDEX.md
# Deve ter formato:
# ## PROJ-XXX
# Status: ...
```

---

### Problema: Estilos não carregam

**Sintoma:** Layout quebrado, sem cores

**Solução:**

```bash
# 1. Verifique conexão com internet
# O dashboard usa Google Fonts e CDN

# 2. Verifique console
# F12 > Console > Network

# 3. Faça download local dos recursos
# (se estiver offline)
```

---

### Problema: Modal não abre

**Sintoma:** Clique em "+ Novo Projeto" não faz nada

**Solução:**

```bash
# 1. Verifique console
# F12 > Console > Errors

# 2. Verifique JavaScript
# Desabilite bloqueadores de script

# 3. Use navegador atualizado
# Chrome 80+ / Firefox 75+
```

---

## Roadmap Futuro

### v1.0 (Atual)
- ✅ Visualização básica
- ✅ Stats
- ✅ Filtros
- ✅ Mobile-first
- ✅ Auto-refresh

### v1.1 (Próxima)
- [ ] Criar projetos reais
- [ ] Editar status
- [ ] Ler STATUS.md de cada projeto
- [ ] Integração com OpenClaw API

### v1.2
- [ ] WebSocket real-time
- [ ] Visualização de PDCA_LOG
- [ ] Detalhes completos do projeto
- [ ] Filtros avançados

### v2.0
- [ ] Autenticação
- [ ] Múltiplos usuários
- [ ] Notificações
- [ ] Relatórios
- [ ] API externa

---

## Glossário

| Termo | Definição |
|-------|-----------|
| **Projeto** | Uma iniciativa com objetivo, prazo e entregáveis |
| **STATUS.md** | Arquivo que contém o estado atual de um projeto |
| **PDCA_LOG** | Log de todas as ações do projeto (Plan-Do-Check-Act) |
| **Gate** | Ponto de aprovação obrigatório no workflow |
| **Tier** | Nível de complexidade do projeto (LITE/MEDIUM/ENTERPRISE) |
| **KSF** | Key Success Factor — critérios de sucesso do projeto |
| **Brainstorming** | Fase inicial de ideação, ainda não é projeto |

---

## Como Contribuir

Para melhorar este dashboard:

1. **Fork** o repositório
2. Crie uma **branch** (`git checkout -b feature/nova-funcionalidade`)
3. Faça **commit** das mudanças
4. Faça **push** para a branch
5. Abra um **Pull Request**

---

## Suporte

Se tiver dúvidas:

1. Leia este manual completo
2. Verifique a [Solução de Problemas](#solução-de-problemas)
3. Verifique o console do navegador (F12 > Console)
4. Entre em contato com o time de desenvolvimento

---

## Licença

Este projeto é parte do **FactoryOS** e segue as mesmas políticas de licenciamento.

---

**Versão:** 1.0
**Última atualização:** 2026-02-12
**Autor:** FactoryOS Team
