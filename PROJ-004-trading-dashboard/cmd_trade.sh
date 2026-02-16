#!/bin/bash
# Trading Analysis Command for Telegram Bot
# Usage: Add this script to bot command handler

cd /home/team/.openclaw/docs/projetos/PROJ-004-trading-dashboard

# Get analysis
python3 -c "
import sys
import json
from datetime import datetime

def analyze_market():
    # In production, call external API
    return {
        'timestamp': datetime.now().isoformat(),
        'market': {
            'symbol': 'BTC/USDT',
            'price': 43250.00,
            'regime': 'sideways',
            'volatility': 'media',
            'trend_strength': 'fraca'
        },
        'recommendation': {
            'acao': 'LONG',
            'perfil': 'swing_trader',
            'setup': 'suporte_resistencia',
            'entrada': 43100.00,
            'tp1': 43800.00,
            'tp2': 44500.00,
            'sl': 42500.00,
            'alavancagem': '1x a 2x',
            'confianca': 'media',
            'score': 65
        },
        'rationale': 'BTC em regime de lateralização. Suporte em \$42,500, resistência em \$44,500.',
        'risk': {
            'stop_loss': 42500.00,
            'risco_por_trade': '1.5%',
            'ratio_risco_retorno': '2.1:1'
        }
    }

a = analyze_market()
m = a['market']
r = a['recommendation']
risk = a['risk']

print(f\"📊 **ANÁLISE DE TRADING**\\n\")
print(f\"**Mercado:**\\n\")
print(f\"- Par: {m['symbol']}\")
print(f\"- Preço: \${m['price']:,.2f}\")
print(f\"- Regime: {m['regime']}\")
print(f\"- Volatilidade: {m['volatility']}\\n\")
print(f\"🎯 **RECOMENDAÇÃO**\\n\")
print(f\"**Ação:** {r['acao']}\")
print(f\"**Perfil:** {r['perfil']}\")
print(f\"**Setup:** {r['setup']}\\n\")
print(f\"📍 **Entrada:** \${r['entrada']:,.2f}\")
print(f\"🎯 **TP1:** \${r['tp1']:,.2f}\")
print(f\"🎯 **TP2:** \${r['tp2']:,.2f}\")
print(f\"🛡️ **SL:** \${r['sl']:,.2f}\")
print(f\"📊 **Alavancagem:** {r['alavancagem']}\")
print(f\"📈 **Confiança:** {r['confianca']} ({r['score']}%)\\n\")
print(f\"⚠️ **Risk:** SL \${risk['stop_loss']:,.2f} | Risco: {risk['risco_por_trade']} | R:R {risk['ratio_risco_retorno']}\")
"
