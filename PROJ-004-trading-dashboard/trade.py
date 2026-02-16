#!/usr/bin/env python3
"""
PROJ-004 Trading Dashboard - Script de Análise e Registro de Trades
用法: python trade.py
"""

import json
import os
from datetime import datetime

ARQUIVO_TRADES = "trades.json"
ARQUIVO_DADOS = "dados_trading.json"

def carregar_trades():
    if os.path.exists(ARQUIVO_TRADES):
        with open(ARQUIVO_TRADES, 'r') as f:
            return json.load(f)
    return []

def salvar_trades(trades):
    with open(ARQUIVO_TRADES, 'w') as f:
        json.dump(trades, f, indent=2)

def calcular_metricas(trades):
    if not trades:
        return {}
    
    total = len(trades)
    wins = len([t for t in trades if t['resultado_pct'] > 0])
    losses = len([t for t in trades if t['resultado_pct'] < 0])
    
    pnl_total = sum(t['resultado_pct'] for t in trades)
    pnl_wins = sum(t['resultado_pct'] for t in trades if t['resultado_pct'] > 0)
    pnl_losses = abs(sum(t['resultado_pct'] for t in trades if t['resultado_pct'] < 0))
    
    win_rate = (wins / total * 100) if total > 0 else 0
    profit_factor = (pnl_wins / pnl_losses) if pnl_losses > 0 else 0
    
    return {
        'total': total,
        'wins': wins,
        'losses': losses,
        'win_rate': win_rate,
        'profit_factor': profit_factor,
        'pnl_medio': pnl_total / total if total > 0 else 0
    }

def analisar_mercado():
    """Análise simples baseada em regras"""
    trades = carregar_trades()
    metricas = calcular_metricas(trades)
    
    print("\n" + "="*50)
    print("📊 ANÁLISE DE TRADING")
    print("="*50)
    
    if metricas:
        print(f"\n📈 Métricas Gerais:")
        print(f"   Total de trades: {metricas['total']}")
        print(f"   Wins: {metricas['wins']} | Losses: {metricas['losses']}")
        print(f"   Win Rate: {metricas['win_rate']:.1f}%")
        print(f"   Profit Factor: {metricas['profit_factor']:.2f}")
        print(f"   PnL Médio: {metricas['pnl_medio']:.2f}%")
    
    # Análise por perfil
    perfis = {}
    for t in trades:
        p = t.get('perfil', 'N/A')
        if p not in perfis:
            perfis[p] = {'wins': 0, 'total': 0, 'pnl': 0}
        perfis[p]['total'] += 1
        if t['resultado_pct'] > 0:
            perfis[p]['wins'] += 1
        perfis[p]['pnl'] += t['resultado_pct']
    
    print(f"\n🎯 Performance por Perfil:")
    for perfil, dados in sorted(perfis.items(), key=lambda x: x[1]['pnl'], reverse=True):
        wr = (dados['wins'] / dados['total'] * 100) if dados['total'] > 0 else 0
        print(f"   {perfil}: {wr:.0f}% WR | PnL: {dados['pnl']:+.1f}%")
    
    # Recomendação simples
    melhor_perfil = max(perfis.items(), key=lambda x: x[1]['pnl']) if perfis else None
    if melhor_perfil:
        print(f"\n🤖 IA Recommendation:")
        print(f"   Perfil recomendado: {melhor_perfil[0]}")
        print(f"   PnL histórico: {melhor_perfil[1]['pnl']:+.1f}%")
    
    return metricas

def registrar_trade():
    print("\n" + "="*50)
    print("📝 REGISTRAR NOVO TRADE")
    print("="*50)
    
    # Data
    data = input("📅 Data (YYYY-MM-DD) [default: hoje]: ").strip()
    if not data:
        data = datetime.now().strftime("%Y-%m-%d")
    
    # Perfil
    print("\n📊 Perfis disponíveis:")
    perfis = ["grid", "trend_alta", "trend_baixa", "lateralizacao", "breakout", "scalp"]
    for i, p in enumerate(perfis, 1):
        print(f"   {i}. {p}")
    
    opcao = input("📌 Perfil: ").strip()
    if opcao.isdigit() and 1 <= int(opcao) <= len(perfis):
        perfil = perfis[int(opcao)-1]
    else:
        perfil = opcao.lower() or "grid"
    
    # Setup
    print("\n🎯 Setups disponíveis:")
    setups = ["scalp_1m", "scalp_5m", "scalp_15m", "daytrade_1h", "daytrade_4h", 
              "swing_1d", "swing_1w", "custom"]
    for i, s in enumerate(setups, 1):
        print(f"   {i}. {s}")
    
    opcao = input("⚡ Setup: ").strip()
    if opcao.isdigit() and 1 <= int(opcao) <= len(setups):
        setup = setups[int(opcao)-1]
    else:
        setup = opcao.lower() or "custom"
    
    # Preços
    entrada = float(input("💰 Preço de entrada: "))
    tp = float(input("🎯 Take Profit: "))
    sl = float(input("🛡️ Stop Loss: "))
    
    # Resultado
    resultado_pct = float(input("📈 Resultado (%): "))
    resultado_usdt = float(input("💵 Resultado (USDT): "))
    
    # Alavancagem
    alavancagem = int(input("📊 Alavancagem (1-125): ") or "1")
    
    trade = {
        "data": data,
        "perfil": perfil,
        "setup": setup,
        "entrada": entrada,
        "tp": tp,
        "sl": sl,
        "resultado_pct": resultado_pct,
        "resultado_usdt": resultado_usdt,
        "alavancagem": alavancagem,
        "timestamp": datetime.now().isoformat()
    }
    
    # Salvar
    trades = carregar_trades()
    trades.append(trade)
    salvar_trades(trades)

    print(f"   Perfil: {perfil}")
    print(f"   Resultado: {resultado_pct:+.2f}% ({resultado_usdt:+.2f} USDT)")
    
    return trade

def menu():
    while True:
        print("\n" + "="*50)
        print("🚀 PROJ-004 TRADING DASHBOARD")
        print("="*50)
        print("1. 📊 Ver análise de trading")
        print("2. 📝 Registrar novo trade")
        print("3. 🚪 Sair")
        
        opcao = input("\n👉 Opção: ").strip()
        
        if opcao == "1":
            analisar_mercado()
        elif opcao == "2":
            registrar_trade()
        elif opcao == "3":
            print("\n👋 Até mais!")
            break
        else:
            print("\n❌ Opção inválida!")
        
        input("\n[Enter para continuar...]")

if __name__ == "__main__":
    menu()
