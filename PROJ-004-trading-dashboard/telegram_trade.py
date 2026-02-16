#!/usr/bin/env python3
"""
Trading Analysis - Real-time data from CoinGecko
"""

import requests
import json
from datetime import datetime

def get_btc_price():
    """Get real BTC price from CoinGecko"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin",
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        return {
            "price": data["bitcoin"]["usd"],
            "change_24h": data["bitcoin"]["usd_24h_change"]
        }
    except Exception as e:
        print(f"Erro ao buscar preço: {e}")
        return None

def get_market_data():
    """Get market regime analysis"""
    btc = get_btc_price()
    
    if not btc:
        return None
    
    price = btc["price"]
    change = btc["change_24h"]
    
    # Simple regime detection
    if change > 2:
        regime = "bull"
        trend = "forte"
        volatility = "alta"
    elif change < -2:
        regime = "bear"
        trend = "forte"
        volatility = "alta"
    else:
        regime = "sideways"
        trend = "fraca"
        volatility = "media"
    
    # Calculate support/resistance
    atr = price * 0.02  # Simple ATR estimate
    support = price - (atr * 2)
    resistance = price + (atr * 2)
    
    return {
        "symbol": "BTC/USDT",
        "price": price,
        "change_24h": change,
        "regime": regime,
        "volatility": volatility,
        "trend_strength": trend,
        "support": round(support, 2),
        "resistance": round(resistance, 2)
    }

def analyze(market):
    """Generate trading recommendation based on market"""
    price = market["price"]
    change = market["change_24h"]
    regime = market["regime"]
    
    # Simple strategy
    if regime == "bull":
        acao = "LONG"
        perfil = "trend_follower"
        setup = "ma_crossover"
        tp_multiplier = 1.03
        sl_multiplier = 0.97
    elif regime == "bear":
        acao = "SHORT"
        perfil = "trend_follower"
        setup = "ma_crossover"
        tp_multiplier = 0.97
        sl_multiplier = 1.03
    else:
        acao = "LONG"
        perfil = "swing_trader"
        setup = "suporte_resistencia"
        tp_multiplier = 1.02
        sl_multiplier = 0.98
    
    entrada = price
    tp1 = price * tp_multiplier
    tp2 = price * (tp_multiplier + 0.02)
    sl = price * sl_multiplier
    
    # Confidence based on regime clarity
    confianca = "alta" if abs(change) > 2 else "media"
    score = 75 if abs(change) > 2 else 65
    
    return {
        "acao": acao,
        "perfil": perfil,
        "setup": setup,
        "entrada": round(entrada, 2),
        "tp1": round(tp1, 2),
        "tp2": round(tp2, 2),
        "sl": round(sl, 2),
        "alavancagem": "1x a 2x",
        "confianca": confianca,
        "score": score
    }

def main():
    print("📊 Buscando dados do mercado...")
    
    market = get_market_data()
    
    if not market:
        print("❌ Erro ao obter dados do mercado")
        return
    
    rec = analyze(market)
    
    print()
    print("="*50)
    print("ANÁLISE DE TRADING - BTC")
    print("="*50)
    print()
    print("MERCADO:")
    print(f"  Par: {market['symbol']}")
    print(f"  Preço: ${market['price']:,.2f}")
    print(f"  24h: {market['change_24h']:+.2f}%")
    print(f"  Regime: {market['regime']}")
    print(f"  Volatilidade: {market['volatility']}")
    print(f"  Trend: {market['trend_strength']}")
    print(f"  Suporte: ${market['support']:,.2f}")
    print(f"  Resistencia: ${market['resistance']:,.2f}")
    print()
    print("RECOMENDAÇÃO:")
    print(f"  Ação: {rec['acao']}")
    print(f"  Perfil: {rec['perfil']}")
    print(f"  Setup: {rec['setup']}")
    print()
    print("ENTRY/EXIT:")
    print(f"  Entrada: ${rec['entrada']:,.2f}")
    print(f"  TP1: ${rec['tp1']:,.2f}")
    print(f"  TP2: ${rec['tp2']:,.2f}")
    print(f"  SL: ${rec['sl']:,.2f}")
    print(f"  Alavancagem: {rec['alavancagem']}")
    print(f"  Confiança: {rec['confianca']} ({rec['score']}%)")

if __name__ == "__main__":
    main()
