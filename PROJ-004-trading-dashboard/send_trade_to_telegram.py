#!/usr/bin/env python3
"""
Send real trading analysis to Telegram
"""

import requests
import json
from datetime import datetime

BOT_TOKEN = "8408398636:AAHhRKBUL-uEHiRBj8D6-M8vSM_d7p5FgN4"
CHAT_ID = "1368659090"

def get_btc_price():
    """Get real BTC price from CoinGecko"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {"ids": "bitcoin", "vs_currencies": "usd", "include_24hr_change": "true"}
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        return {
            "price": data["bitcoin"]["usd"],
            "change_24h": data["bitcoin"]["usd_24h_change"]
        }
    except Exception as e:
        print(f"Erro: {e}")
        return None

def analyze():
    btc = get_btc_price()
    if not btc:
        return None
    
    price = btc["price"]
    change = btc["change_24h"]
    
    # Regime detection
    if change > 2:
        regime, trend, vol = "BULL", "forte", "alta"
        acao, perfil, setup = "LONG", "trend_follower", "ma_crossover"
        tp_mult, sl_mult = 1.03, 0.97
    elif change < -2:
        regime, trend, vol = "BEAR", "forte", "alta"
        acao, perfil, setup = "SHORT", "trend_follower", "ma_crossover"
        tp_mult, sl_mult = 0.97, 1.03
    else:
        regime, trend, vol = "SIDEWAYS", "fraca", "media"
        acao, perfil, setup = "LONG", "swing_trader", "suporte_resistencia"
        tp_mult, sl_mult = 1.02, 0.98
    
    atr = price * 0.02
    support = round(price - atr * 2, 2)
    resistance = round(price + atr * 2, 2)
    
    rec = {
        "acao": acao, "perfil": perfil, "setup": setup,
        "entrada": price,
        "tp1": round(price * tp_mult, 2),
        "tp2": round(price * (tp_mult + 0.02), 2),
        "sl": round(price * sl_mult, 2),
        "alavancagem": "1x a 2x",
        "confianca": "alta" if abs(change) > 2 else "media",
        "score": 75 if abs(change) > 2 else 65
    }
    
    market = {
        "symbol": "BTC/USDT", "price": price, "change_24h": change,
        "regime": regime, "volatility": vol, "trend_strength": trend,
        "support": support, "resistance": resistance
    }
    
    return market, rec

def send_to_telegram(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": text, "parse_mode": "Markdown"}
    response = requests.post(url, json=data)
    return response.json()

def format_message(market, rec):
    return f"""📊 *ANÁLISE DE TRADING*

*{market['symbol']}* - ${market['price']:,.2f} ({market['change_24h']:+.2f}%)

*Regime:* {market['regime']} | *Vol:* {market['volatility']} | *Trend:* {market['trend_strength']}

━━━━━━━━━━━━━━━━━━━━

🎯 *RECOMENDAÇÃO*

*{rec['acao']}* | {rec['perfil']} | {rec['setup']}

📍 *Entrada:* ${rec['entrada']:,.2f}
🎯 *TP1:* ${rec['tp1']:,.2f} | *TP2:* ${rec['tp2']:,.2f}
🛡️ *SL:* ${rec['sl']:,.2f}
📊 *Alavancagem:* {rec['alavancagem']}
📈 *Confiança:* {rec['confianca']} ({rec['score']}%)

━━━━━━━━━━━━━━━━━━━━

💰 *Suporte:* ${market['support']:,.2f}
💰 *Resistência:* ${market['resistance']:,.2f}"""

def main():
    print("📊 Gerando análise...")
    result = analyze()
    if not result:
        print("❌ Erro ao obter dados")
        return
    
    market, rec = result
    message = format_message(market, rec)
    
    print("\n📤 Enviando...")
    result = send_to_telegram(message)
    
    if result.get('ok'):
        print("✅ Enviado!")
    else:
        print(f"❌ Erro: {result}")

if __name__ == "__main__":
    main()
