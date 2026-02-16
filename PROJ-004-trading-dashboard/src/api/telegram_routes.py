from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import json

router = APIRouter()

# Simulated market analysis (in production, call CoinGecko API)
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
        "rationale": "BTC em regime de lateralização. Suporte em $42,500, resistência em $44,500.",
        "risk": {
            "stop_loss": 42500.00,
            "risco_por_trade": "1.5%",
            "ratio_risco_retorno": "2.1:1"
        }
    }

@router.get("/analise")
async def get_analysis():
    """Get trading analysis from crypto_analyst"""
    return analyze_market()

@router.post("/trades")
async def register_trade(trade: dict):
    """Register a new trade"""
    # Load existing trades
    try:
        with open("trades.json", "r") as f:
            trades = json.load(f)
    except:
        trades = []
    
    # Add new trade
    trade["timestamp"] = datetime.now().isoformat()
    trades.append(trade)
    
    # Save
    with open("trades.json", "w") as f:
        json.dump(trades, f, indent=2)
    
    return {"status": "success", "trade": trade}

@router.get("/trades")
async def get_trades():
    """Get all trades"""
    try:
        with open("trades.json", "r") as f:
            return {"trades": json.load(f)}
    except:
        return {"trades": []}

@router.get("/performance")
async def get_performance():
    """Get performance metrics"""
    try:
        with open("trades.json", "r") as f:
            trades = json.load(f)
    except:
        return {"error": "No trades found"}
    
    if not trades:
        return {"error": "No trades recorded"}
    
    wins = len([t for t in trades if t.get("resultado_pct", 0) > 0])
    losses = len([t for t in trades if t.get("resultado_pct", 0) < 0])
    total = len(trades)
    pnl = sum([t.get("resultado_pct", 0) for t in trades])
    
    return {
        "total_trades": total,
        "wins": wins,
        "losses": losses,
        "win_rate": f"{(wins/total*100):.1f}%" if total > 0 else "0%",
        "pnl_total": f"{pnl:+.2f}%",
        "wins_trades": [t for t in trades if t.get("resultado_pct", 0) > 0][-5:] if wins > 0 else [],
        "losses_trades": [t for t in trades if t.get("resultado_pct", 0) < 0][-5:] if losses > 0 else []
    }
