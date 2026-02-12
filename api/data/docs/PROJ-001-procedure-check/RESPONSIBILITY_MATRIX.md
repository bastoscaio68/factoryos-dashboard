# RESPONSIBILITY MATRIX — PROJ-001

> Gate 3 — obrigatório para ENTERPRISE.
> Fonte da verdade para dependências e sequência de execução.

---

## RESUMO DO PROJETO

| Campo | Valor |
|---|---|
| Projeto | PROJ-001 — Procedure Check + Marketing Visual |
| Tier | ENTERPRISE |
| Fase atual | Planejamento |
| Última atualização | 2026-02-12 00:27 \| orquestrador |

---

## MATRIZ DE FASES E ENTREGÁVEIS

| # | Fase / Entregável | Agente Owner | Input Necessário | Output / Artefato | Prazo | Status | Observações |
|---|---|---|---|---|---|---|---|
| 01 | Validação Estratégica | brain | REQUEST_PROJ-001.md | Recomendações estratégicas | D+0 | ⏳ | Paralelo |
| 02 | Precificação do Material | sales/pricing_engine | REQUEST_PROJ-001.md | Breakdown de custos | D+0 | ⏳ | Paralelo |
| 03 | Criação da Proposta | sales/proposal_generator | Precificação | PROPOSTA-001.md | D+0 | ⏳ | Paralelo |
| 04 | Requisitos do Material | engineering/scope_parser | REQUEST_PROJ-001.md | REQ-001.md | D+0 | ⏳ | |
| 05 | Referências Visuais | intelligence/scraper | - | DADOS-COLETADOS.md | D+0 | ✅ | |
| 06 | Tendências de Design | intelligence/trend_analyst | Dados do scraper | TREND-REPORT.md | D+0 | ⏳ | |
| 07 | Análise de Mercado | trading/crypto_analyst | - | MARKET-BRIEF.md | D+0 |🔄 | |
| 08 | Cronograma | pmo/scheduler | REQ-001.md | GANTT-001.md | D+0 | ⏳ | |
| 09 | Identidade Visual | design/brand_system | - | BRAND-GUIDE.md | D+1 |⏳ | Depende 01-04 |
| 10 | Pautas de Conteúdo | content/ideation | TREND-REPORT.md | PAUTAS-001.md | D+1 | ⏳ | Depende 06 |
| 11 | Texts Marketing | content/copywriter | PAUTAS-001.md | TEXTS-001.md | D+2 | ⏳ | Depende 10 |
| 12 | Revisão de Texts | content/editor | TEXTS-001.md | TEXTS-APPROVED.md | D+2 | ⏳ | Depende 11 |
| 13 | Slides/HTML | design/presentation_builder | BRAND-GUIDE + TEXTS-APPROVED | SLIDES-001.html | D+2 | ⏳ | Depende 09, 12 |
| 14 | Validação de Risco | trading/risk_manager | MARKET-BRIEF.md | RISK-APPROVE.md | D+1 | ⏳ | Depende 07 |
| 15 | QA Final | pmo/quality_auditor | SLIDES-001.html + RISK-APPROVE | QA-REPORT.md | D+3 | ⏳ | Depende 13, 14 |
| 16 | Preparação para Entrega | content/distribution | SLIDES-001.html | READY-FOR-DELIVERY.md | D+3 | ⏳ | Depende 15 |
| 17 | Faturamento Interno | finance/billing | - | INVOICE-001.md | D+3 |⏳ |
| 18 | Relatório de Projeto | finance/pnl_report | INVOICE-001.md + QA-REPORT | PNL-001.md | D+3 | ⏳ | Depende 17 |

---

## DEPENDÊNCIAS CRÍTICAS

```
brain ──────────┬──────────→ sales/pricing_engine
                │
                ├──→ engineering/scope_parser
                │
                ├──→ intelligence/scraper
                │
                └──→ trading/crypto_analyst

engineering/scope_parser ──→ pmo/scheduler
                            │
intelligence/scraper ──────→ intelligence/trend_analyst
                            │
                            └──→ content/ideation

content/ideation ────────→ content/copywriter
                        │
                        └──→ content/editor
                            │
                            └──→ design/presentation_builder
                                │
                                ├──→ design/brand_system
                                │
                                └──→ trading/risk_manager

design/presentation_builder ───→ pmo/quality_auditor
                                │
trading/risk_manager ─────────→ pmo/quality_auditor

pmo/quality_auditor ────────→ content/distribution
                                │
                                └──→ finance/billing
                                    │
                                    └──→ finance/pnl_report
```

---

## AGENTES ATIVOS NESTE PROJETO

| Agente | Função no Projeto | Fases | Status |
|---|---|---|---|
| orquestrador | Coordenação e monitoramento | Todas | ⏳ |
| brain | Validação estratégica | 01 | ⏳ |
| sales/pricing_engine | Precificação | 02 | ⏳ |
| sales/proposal_generator | Proposta interna | 03 | ⏳ |
| engineering/scope_parser | Requisitos | 04 | ⏳ |
| intelligence/scraper | Coleta de dados | 05 | ⏳ |
| intelligence/trend_analyst | Análise de tendências |⏳  06 | ⏳ |
| trading/crypto_analyst | Análise de mercado | 07 | ⏳ |
| pmo/scheduler | Cronograma |⏳  08 |🔄 |
| content/ideation | Pautas |⏳  10 | ⏳ |
| content/copywriter | Texts | 11 | ⏳ |
| content/editor | Revisão | 12 | ⏳ |
| design/presentation_builder | Slides/HTML | 13 | ⏳ |
| trading/risk_manager | Validação de risco | 14 | ⏳ |
| pmo/quality_auditor | QA Final | 15 | ⏳ |
| content/distribution | Preparação | 16 | ⏳ |
| finance/pnl_report | Relatório | 18 |⏳ |

---

## AGENTES EM STANDBY

| Agente | Condição de Ativação |
|---|---|
| ops/bot_manager | Se automações necessárias |
| ops/market_monitor | Se integrações externas necessárias |
| life_os/daily_planner | Para acompanhamento diário |
| life_os/habit_tracker | Registro de progresso |
| engineering/calc_engine | Não necessário neste projeto |
| engineering/drawing_generator | Não necessário neste projeto |
| trading/trader | Mock only — sem trades reais |

---

## LOG DE MUDANÇAS DE ESCOPO

[APPEND ONLY — registrar mudanças]

[2026-02-12] orquestrador: Projeto interno aprovado. Scope: testar todas as rotas + material de marketing. | Impacto: todos os agentes envolvidos

---

## OBSERVAÇÕES

- Projeto ENTERPRISE requer monitoramento contínuo do orquestrador
- Communications failures devem ser documentados no PDCA_LOG
- Brain deve ser acionado para validação estratégica
