#!/usr/bin/env python3
"""
Simple Flask API for Telegram Bot Commands
Run: python3 bot_api.py
"""

from flask import Flask, jsonify, request
from datetime import datetime
import json

app = Flask(__name__)

TRADES_FILE = "trades.json"

def load_trades():
    try:
        with open(TRADES_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

def save_trade(trade):
    trades = load_trades()
    trade['timestamp'] = datetime.now().isoformat()
    trades.append(trade)
    with open(TRADES_FILE, 'w') as f:
        json.dump(trades, f, indent=2)
    return trade

def analyze_market():
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

@app.route('/')
def home():
    return jsonify({
        "status": "ok",
        "endpoints": {
            "/analise": "Get trading analysis",
            "/trades": "Get all trades",
            "/trades POST": "Register a trade",
            "/performance": "Get performance metrics"
        }
    })

@app.route('/analise')
def get_analise():
    """Return analysis formatted for Telegram"""
    a = analyze_market()
    m = a['market']
    r = a['recommendation']
    risk = a['risk']
    
    text = f"""📊 **ANÁLISE DE TRADING**

**Mercado:**
- Par: {m['symbol']}
- Preço: ${m['price']:,.2f}
- Regime: {m['regime']}
- Volatilidade: {m['volatility']}
- Trend: {m['trend_strength']}

🎯 **RECOMENDAÇÃO**
**Ação:** {r['acao']} | **Perfil:** {r['perfil']} | **Setup:** {r['setup']}

📍 **Entrada:** ${r['entrada']:,.2f}
🎯 **TP1:** ${r['tp1']:,.2f} | **TP2:** ${r['tp2']:,.2f}
🛡️ **SL:** ${r['sl']:,.2f}
📊 **Alavancagem:** {r['alavancagem']}
📈 **Confiança:** {r['confianca']} ({r['score']}%)

⚠️ **Risk:** SL ${risk['stop_loss']:,.2f} | R:R {risk['ratio_risco_retorno']}"""
    
    return jsonify({"text": text, "data": a})

@app.route('/trades', methods=['GET'])
def get_trades():
    return jsonify({"trades": load_trades()})

@app.route('/trades', methods=['POST'])
def post_trade():
    trade = request.json
    saved = save_trade(trade)
    return jsonify({"status": "success", "trade": saved})

@app.route('/performance')
def get_performance():
    trades = load_trades()
    if not trades:
        return jsonify({"error": "No trades"})
    
    wins = len([t for t in trades if t.get("resultado_pct", 0) > 0])
    losses = len([t for t in trades if t.get("resultado_pct", 0) < 0])
    total = len(trades)
    pnl = sum([t.get("resultado_pct", 0) for t in trades])
    
    return jsonify({
        "total": total,
        "wins": wins,
        "losses": losses,
        "win_rate": f"{(wins/total*100):.1f}%" if total > 0 else "0%",
        "pnl_total": f"{pnl:+.2f}%"
    })

if __name__ == '__main__':
    print("🚀 Bot API rodando em http://localhost:5000")
    app.run(port=5000, debug=True)
