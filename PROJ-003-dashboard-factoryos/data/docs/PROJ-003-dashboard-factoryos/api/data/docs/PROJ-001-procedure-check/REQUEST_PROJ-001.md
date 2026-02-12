# PROJECT REQUEST — PROJ-001

> Gate 1 obrigatório para projetos ENTERPRISE.
> Sem este documento aprovado pelo humano, o projeto não inicia.

---

## IDENTIFICAÇÃO

| Campo | Valor |
|-------|-------|
| ID do Projeto | PROJ-001 |
| Nome | Procedure Check + Marketing Visual |
| Data da Request | 2026-02-12 |
| Solicitante | Humano (Caio Bastos) |
| Tier | 🔴 ENTERPRISE |
| Departamento Principal | INTERNAL (todos os departamentos) |
| Orquestrador responsável | orquestrador |

---

## OBJETIVO DO PROJETO

Criar um projeto interno de "stress test" completo do FactoryOS para verificar se todas as rotas de comunicação entre os 26 agentes funcionam corretamente, produzindo um **material de marketing visual** que demonstra todo o processo da empresa desde a entrada de um pedido até a entrega final — Feito para impressionar futuros clientes.

---

## ENTREGÁVEIS ESPERADOS

- [ ] **Material de Marketing Visual** — Apresentação/slides demonstrando:
  - Fluxo completo do FactoryOS
  - Cada departamento em ação
  - Comunicações entre agentes
  - Timeline do projeto
  - Feito para impressionar futuros clientes
- [ ] **Documentation** — Registro em PDCA_LOG de todas as decisões e comunicações
- [ ] **Procedure Report** — Relatório de "lessons learned" com gaps identificados

---

## CLIENTE / DESTINATÁRIO

| Campo | Valor |
|-------|-------|
| Nome/Empresa | FactoryOS (interno) |
| ID do Cliente | CLI-INTERNAL |
| Contato | humano |
| Contexto interno | Projeto de verificação de sistema |

---

## ESCOPO

### Incluso

- Uso de TODOS os 26 agentes do sistema
- Comunicação entre todos os departamentos
- Execução de pipeline completo
- Documentação visual do processo
- Registro de gaps e correções

### Excluído

- Projetos externos reais
- Billing com cliente externo
- Entrega para cliente real

### Premissas

- Projeto é de teste interno — não requer cliente real
- Todos os agentes devem ser acionados pelo menos uma vez
- Material visual é "demo" para futuros clientes

---

## PRAZO

| Marco | Data |
|-------|-------|
| Início | 2026-02-12 |
| Entrega final | 2026-02-14 |
| Prazo do cliente | N/A (interno) |

---

## BUDGET

| Campo | Valor |
|-------|-------|
| Valor orçado | US$ 0 (interno) |
| Modelo de precificação | N/A (projeto interno) |
| Proposta enviada? | N/A |
| Aprovação de budget | ✅ Aprovado (interno) |

---

## AGENTES NECESSÁRIOS (TODOS)

| Agente | Papel | Fase |
|--------|-------|------|
| orquestrador | Coordenação geral | Todas |
| brain | Validação estratégica | Início |
| sales/pricing_engine | Precificação do material | Início |
| sales/proposal_generator | Criação da proposta interna | Início |
| engineering/scope_parser | Definir requisitos do material | Fase 1 |
| engineering/calc_engine | Dimensionamento técnico | Fase 1 |
| engineering/drawing_generator | Especificações visuais | Fase 1 |
| content/ideation | Gerar conteúdo descritivo | Fase 2 |
| content/copywriter | Redigir textos | Fase 2 |
| content/editor | Revisão | Fase 2 |
| content/distribution | Preparar para apresentação | Fase 3 |
| design/brand_system | Identidade visual | Fase 2 |
| design/presentation_builder | Criar apresentação HTML | Fase 3 |
| pmo/scheduler | Cronograma do projeto | Fase 1 |
| pmo/quality_auditor | QA em todas as fases | Contínuo |
| ops/bot_manager | Verificar automações | Fase 2 |
| ops/market_monitor | Validar integrações | Fase 2 |
| intelligence/scraper | Coletar referências | Fase 1 |
| intelligence/trend_analyst | Analisar tendências de design | Fase 1 |
| trading/crypto_analyst | Análise de mercado (contexto) | Fase 1 |
| trading/risk_manager | Validação de risco | Fase 1 |
| trading/trader | Execução de trades (mock) | Fase 1 |
| finance/billing | Registrar custo interno | Fim |
| finance/pnl_report | Relatório financeiro (mock) | Fim |
| life_os/daily_planner | Planejamento diário | Contínuo |
| life_os/habit_tracker | Registro de progresso | Contínuo |

---

## RISCOS IDENTIFICADOS

| Risco | Probabilidade | Impacto | Mitigação |
|-------|--------------|---------|-----------|
| Agente não responde | Média | Baixo | Documentar gap, prosseguir |
| Rota de comunicação falhar | Média | Médio | Identificar e corrigir |
| Dependência circular | Baixa | Alto | Seguir hierarquia definida |
| QA reprova output | Baixa | Médio | Revisar antes de enviar |

---

## CRITÉRIOS DE SUCESSO (KSFs)

- KSF 1: Todos os 26 agentes foram acionados pelo menos uma vez
- KSF 2: Material de marketing visual produzido (slides/HTML/demonstrativo)
- KSF 3: Zero erros de comunicação (routing) entre agentes
- KSF 4: Projeto concluído em 48h

---

## APROVAÇÃO

| Campo | Valor |
|-------|-------|
| Aprovado por | Humano (Caio Bastos) |
| Data de aprovação | 2026-02-12 |
| Status | ✅ Aprovado |
| Observações | Projeto interno de stress test |

---

> **Após aprovação:** Orquestrador cria estrutura de pastas (Gate 3) e inicia execução.
