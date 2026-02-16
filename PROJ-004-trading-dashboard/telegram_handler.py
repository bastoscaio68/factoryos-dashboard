#!/usr/bin/env python3
"""
Telegram Bot Command Handler for /trade
Usage: Add this to your bot's command handler
"""

import sys
import json
from datetime import datetime

def analyze():
    """Get trading analysis"""
    # In production, this could call external APIs
    return {
        "timestamp": datetime.now().isoformat(),
        "market": {
            "symbol": "BTC/USDT",
            "price": 43250.00,
            "regime": "sideways",
            "volatility": "media",
            "trend_strength": "fraca"
        },
        "recommendation": {
            "acao": "LONG",
            "perfil": "swing_trader",
            "setup": "suporte_resistencia",
            "entrada": 43100.00,
            "tp1": 43800.00,
            "tp2": 44500.00,
            "sl": 42500.00,
            "alavancagem": "1x a 2x",
            "confianca": "media",
            "score": 65
        },
        "risk": {
            "stop_loss": 42500.00,
            "risco_por_trade": "1.5%",
            "ratio_risco_retorno": "2.1:1"
        }
    }

def format_for_telegram(data):
    m = data['market']
    r = data['recommendation']
    risk = data['risk']
    
    return f"""📊 **ANÁLISE DE TRADING**

**Mercado:**
• {m['symbol']}: ${m['price']:,.2f}
• Regime: {m['regime']}
• Volatilidade: {m['volatility']}
• Trend: {m['trend_strength']}

🎯 **RECOMENDAÇÃO**
**{r['acao']}** | {r['perfil']} | {r['setup']}

📍 ${r['entrada']:,.2f} → 🎯 ${r['tp1']:,.2f}/{r['tp2']:,.2f}
🛡️ SL: ${r['sl']:,.2f}
📊 {r['alavancagem']} | Confiança: {r['confianca']} ({r['score']}%)

⚠️ Risk: {risk['risco_por_trade']} | R:R {risk['ratio_risco_retorno']}"""

def register_trade(data):
    """Register a trade from Telegram"""
    trade = {
        "data": data.get("data", ""),
        "perfil": data.get("perfil", ""),
        "setup": data.get("setup", ""),
        "entrada": data.get("entrada", 0),
        "tp": data.get("tp", 0),
        "sl": data.get("sl", 0),
        "resultado_pct": data.get("resultado_pct", 0),
        "resultado_usdt": data.get("resultado_usdt", 0),
        "alavancagem": data.get("alavancagem", 1),
        "status": data.get("status", "aberto")
    }
    
    # Save to file
    try:
        with open("trades.json", "r") as f:
            trades = json.load(f)
    except:
        trades = []
    
    trades.append(trade)
    
    with open("trades.json", "w") as f:
        json.dump(trades, f, indent=2)
    
    return f"✅ Trade registrado!\n\nPerfil: {trade['perfil']}\nEntrada: ${trade['entrada']}\nStatus: {trade['status']}"

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 telegram_handler.py <command> [args]")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "analise":
        data = analyze()
        print(format_for_telegram(data))
    elif cmd == "registrar":
        if len(sys.argv) > 2:
            data = json.loads(sys.argv[2])
            print(register_trade(data))
        else:
            print("Usage: python3 telegram_handler.py registrar <json_data>")
    elif cmd == "performance":
        try:
            with open("trades.json", "r") as f:
                trades = json.load(f)
        except:
            print("Nenhum trade registrado")
            sys.exit(0)
        
        wins = len([t for t in trades if t.get("resultado_pct", 0) > 0])
        losses = len([t for t in trades if t.get("resultado_pct", 0) < 0])
        total = len(trades)
        pnl = sum([t.get("resultado_pct", 0) for t in trades])
        
        print(f"""📈 **PERFORMANCE**
Trades: {total} | Wins: {wins} | Losses: {losses}
Win Rate: {(wins/total*100):.1f}%" if total > 0 else "0%"}
PnL Total: {pnl:+.2f}%""")
    else:
        print(f"Unknown command: {cmd}")
