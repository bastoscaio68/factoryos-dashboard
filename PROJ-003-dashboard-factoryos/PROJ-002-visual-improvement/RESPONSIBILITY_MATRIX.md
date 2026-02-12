# RESPONSIBILITY MATRIX — PROJ-002

> Gate 3 — obrigatório para ENTERPRISE.
> Fonte da verdade para dependências e sequência de execução.

---

## RESUMO DO PROJETO

| Campo | Valor |
|-------|-------|
| Projeto | PROJ-002 — Melhoria da Qualidade Visual |
| Tier | ENTERPRISE |
| Fase atual | Planejamento |
| Última atualização | 2026-02-12 06:10 |

---

## MATRIZ DE FASES E ENTREGÁVEIS

| # | Fase / Entregável | Agente Owner | Input Necessário | Output / Artefato | Prazo | Status | Observações |
|---|---|---|---|---|---|---|---|
| 01 | Diagnóstico Visual | brain | Feedback do Caio | DIAGNOSTICO-VISUAL.md | D+0 | ⏳ | |
| 02 | Catálogo de Ferramentas | ideation | - | FERRAMENTAS-CATALOG.md | D+0 | ⏳ | |
| 03 | Custos e Budget | pricing_engine | FERRAMENTAS-CATALOG.md | BUDGET-DETALHADO.md | D+0 | ⏳ | |
| 04 | Guia de Implementação | scope_parser | DIAGNOSTICO-VISUAL.md | GUIA-IMPLEMENTACAO.md | D+0 | ⏳ | |
| 05 | Roadmap de Execução | scheduler | Todos acima | ROADMAP.md | D+0 | ⏳ | |
| 06 | Templates de Exemplo | presentation_builder | GUIA-IMPLEMENTACAO.md | TEMPLATES-EXEMPLOS | D+1 | ⏳ | |
| 07 | QA Final | quality_auditor | Todos artefatos | QA-REPORT.md | D+1 | ⏳ | |

---

## DEPENDÊNCIAS CRÍTICAS

```
brain ──────────→ ideation ──────────→ pricing_engine
                                    │
scope_parser ────┘                  │
                                    ↓
                          scheduler ──→ presentation_builder

brain ────────────────────────────────────────────────────→ quality_auditor
scope_parser ──────────────────────────────────────────────→ quality_auditor
pricing_engine ────────────────────────────────────────────→ quality_auditor
presentation_builder ───────────────────────────────────────→ quality_auditor
```

---

## AGENTES ATIVOS NESTE PROJETO

| Agente | Função no Projeto | Fases | Status |
|---|---|---|---|
| orquestrador | Coordenação | Todas | ⏳ |
| brain | Diagnóstico estratégico | 01 | ⏳ |
| ideation | Catálogo de ferramentas | 02 | ⏳ |
| pricing_engine | Custos e budget | 03 | ⏳ |
| scope_parser | Guia de implementação | 04 | ⏳ |
| scheduler | Roadmap | 05 | ⏳ |
| presentation_builder | Templates exemplos | 06 | ⏳ |
| quality_auditor | QA Final | 07 | ⏳ |

---

## AGENTES EM STANDBY

| Agente | Condição de Ativação |
|---|---|
| design/brand_system | Para design system mais robusto |
| design/brand_system | Criação de assets customizados |

---

## LOG DE MUDANÇAS DE ESCOPO

[APPEND ONLY — registrar mudanças]

[2026-02-12] orquestrador: Projeto iniciado a partir do feedback do Caio sobre qualidade visual do SLIDES-001.html | Impacto: Seleção de ferramentas e roadmap de melhoria

---

## OBSERVAÇÕES

- Projeto ENTERPRISE requer monitoramento contínuo do orquestrador
- Ferramentas gratis devem ser priorizadas
- Curva de aprendizado deve ser considerada
- Manutenção contínua deve ser documentada
