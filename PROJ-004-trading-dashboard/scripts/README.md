# Script /trade - Registro de Trades

CLI para registro rápido de trades no PROJ-004 Trading Dashboard.

## Instalação

```bash
# Tornar o script executável
chmod +x docs/projetos/PROJ-004-trading-dashboard/scripts/trade.py

# Opcional: criar alias ou link simbólico
ln -s docs/projetos/PROJ-004-trading-dashboard/scripts/trade.py /usr/local/bin/trade
```

## Dependências

```bash
pip install requests
```

## Variáveis de Ambiente

Configure as variáveis de ambiente antes de usar:

```bash
export API_BASE_URL="http://localhost:3000/api"
export API_TOKEN="your-api-token"
```

## Uso

### Modo Interativo

```bash
python docs/projetos/PROJ-004-trading-dashboard/scripts/trade.py --interactive
```

O script solicitará os seguintes campos:
- Data/Hora do trade (ISO format)
- Perfil do trade
- Resultado em %
- Resultado em USDT
- Alavancagem
- Setup utilizado
- Preço de entrada
- Take Profit
- Stop Loss
- Notas (opcional)

### Via JSON (linha de comando)

```bash
python trade.py --json '{
  "datetime": "2024-01-15T14:30:00",
  "profile": "trend_alta",
  "result_percent": 2.5,
  "result_usdt": 125.0,
  "leverage": 10,
  "setup": "scalp_1m",
  "entry": 43250.50,
  "tp": 43500.00,
  "sl": 43000.00,
  "notes": "Trade clássico de momentum"
}'
```

### Via Arquivo JSON

```bash
python trade.py --file trades.json
```

Formato do arquivo `trades.json`:
```json
[
  {
    "datetime": "2024-01-15T14:30:00",
    "profile": "trend_alta",
    "result_percent": 2.5,
    "result_usdt": 125.0,
    "leverage": 10,
    "setup": "scalp_1m",
    "entry": 43250.50,
    "tp": 43500.00,
    "sl": 43000.00
  }
]
```

## Campos Obrigatórios

| Campo | Tipo | Descrição | Validação |
|-------|------|-----------|-----------|
| `datetime` | string | Data e hora do trade | ISO 8601 |
| `profile` | string | Perfil da operação | Ver perfis válidos |
| `result_percent` | number | Resultado em porcentagem | Qualquer número |
| `result_usdt` | number | Resultado em USDT | Qualquer número |
| `leverage` | integer | Alavancagem utilizada | 1-125 |
| `setup` | string | Setup operacional | Ver setups válidos |
| `entry` | number | Preço de entrada | > 0 |
| `tp` | number | Take Profit | > entry (long) |
| `sl` | number | Stop Loss | < entry (long) |

## Perfils Válidos

| Perfil | Descrição |
|--------|-----------|
| `grid` | Operações em grid |
| `trend_alta` | Tendência de alta |
| `trend_baixa` | Tendência de baixa |
| `lateralizacao` | Mercado lateral |
| `breakout` | Quebra de estrutura |

## Setups Válidos

| Setup | Timeframe |
|-------|-----------|
| `scalp_1m` | 1 minuto |
| `scalp_5m` | 5 minutos |
| `scalp_15m` | 15 minutos |
| `daytrade_1h` | 1 hora |
| `daytrade_4h` | 4 horas |
| `swing_1d` | Diário |
| `swing_1w` | Semanal |
| `custom` | Personalizado |

## Opções Adicionais

### Salvar Apenas Localmente

```bash
python trade.py --json '...' --save-only
```

Útil quando a API não está disponível. Os trades são salvos em `trades_local.json`.

### URL Personalizada da API

```bash
python trade.py --json '...' --api-url "http://custom-api:3000/api"
```

## Validação Automática

O script valida automaticamente:
- ✅ Formato de data/hora
- ✅ Perfis válidos
- ✅ Setups válidos
- ✅ Alavancagem (1-125)
- ✅ Preços positivos
- ✅ Relação TP/SL com entrada

## Fluxo de Execução

```
1. Coletar dados (interativo/JSON/arquivo)
2. Validar todos os campos
3. Mostrar resumo do trade
4. Confirmar com usuário
5. Enviar para API
6. Backup local em caso de falha
```

## Códigos de Saída

| Código | Significado |
|--------|-------------|
| 0 | Sucesso |
| 1 | Erro de validação ou execução |

## Exemplos Completos

### Trade Winner

```bash
$ python trade.py --interactive

=== Registro de Trade ===

Data/Hora [2024-01-15T14:30:00]: 
Perfis válidos: grid, trend_alta, trend_baixa, lateralizacao, breakout
Perfil: trend_alta
Resultado (%): 2.5
Resultado (USDT): 125.0
Alavancagem (1-125): 10
Setups válidos: scalp_1m, scalp_5m, scalp_15m, daytrade_1h, daytrade_4h, swing_1d, swing_1w, custom
Setup: scalp_5m
Entrada: 43250.50
Take Profit (TP): 43500.00
Stop Loss (SL): 43000.00
Notas (opcional): Rompeu resistência em 43100

=== Validação ===
✅ Dados válidos!

=== Resumo do Trade ===
Data/Hora: 2024-01-15T14:30:00
Perfil: trend_alta
Resultado: 2.5% (125.0 USDT)
Alavancagem: 10x
Setup: scalp_5m
Entrada: 43250.5 | TP: 43500.0 | SL: 43000.0

=== Enviando para API ===
✅ Trade registrado com sucesso na API!
ID: trade_abc123
```

### Trade Loser (com erro de validação)

```bash
$ python trade.py --json '{"datetime": "invalid", "profile": "invalid", "leverage": 200}'

=== Validação ===
❌ Erros de validação:
  - Data/hora inválida: invalid. Use formato ISO: YYYY-MM-DDTHH:MM:SS
  - Perfil inválido: invalid. Valores válidos: grid, trend_alta, trend_baixa, lateralizacao, breakout
  - Alavancagem deve ser um inteiro entre 1 e 125
```

## Integração com API

O script espera que a API exponha o endpoint:

```
POST /api/trades
Authorization: Bearer <token>
Content-Type: application/json

{
  "datetime": "2024-01-15T14:30:00",
  "profile": "trend_alta",
  ...
}
```

Response esperado (201 Created):
```json
{
  "id": "trade_abc123",
  "status": "created",
  "created_at": "2024-01-15T14:31:00Z"
}
```

## Troubleshooting

### "Module not found: requests"

```bash
pip install requests
```

### "API Error: 401"

Verifique a variável `API_TOKEN` ou passe via `--api-url` com token embutido.

### "API Error: 500"

A API pode estar offline. O script salvará automaticamente localmente como backup.

## Roadmap

- [ ] Suporte a múltiplos trades em batch
- [ ] Exportação para CSV/Excel
- [ ] Integração direta com APIs de exchange
- [ ] Histórico local com SQLite
