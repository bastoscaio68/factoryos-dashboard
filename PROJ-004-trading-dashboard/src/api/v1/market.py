from typing import List, Optional, Dict
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Query

from src.services.coinGecko_client import get_coingecko_client, CoinGeckoClient
from src.services.regime_detection import regime_detection_engine
from src.services.setup_recommendation import setup_recommendation_engine
from src.schemas import (
    PriceResponse, PriceHistoryResponse, MultiPriceResponse,
    MarketRegimeResponse, SetupRecommendationResponse
)

router = APIRouter(prefix="/market", tags=["Market"])


@router.get("/price/{symbol}", response_model=PriceResponse)
async def get_price(
    symbol: str,
    vs_currency: str = Query(default="usd")
):
    """Obtém preço atual de um ativo."""
    client = get_coingecko_client()
    try:
        # Map symbol to CoinGecko ID
        symbol_map = {
            "BTC": "bitcoin",
            "ETH": "ethereum",
            "SOL": "solana",
            "ADA": "cardano",
            "DOT": "polkadot"
        }
        coin_id = symbol_map.get(symbol.upper(), symbol.lower())
        
        data = await client.get_price(
            ids=[coin_id],
            vs_currencies=[vs_currency],
            include_24hr_change=True,
            include_24hr_vol=True,
            include_market_cap=True
        )
        
        coin_data = data.get(coin_id, {})
        return PriceResponse(
            symbol=symbol.upper(),
            price=coin_data.get(vs_currency, 0),
            change_24h=coin_data.get(f"{vs_currency}_24h_change"),
            volume_24h=coin_data.get(f"{vs_currency}_24h_vol"),
            market_cap=coin_data.get(f"{vs_currency}_market_cap"),
            timestamp=datetime.now(timezone.utc)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erro ao obter preço: {str(e)}"
        )


@router.get("/multi", response_model=MultiPriceResponse)
async def get_multi_prices(
    symbols: str = Query(..., description="Símbolos separados por vírgula, ex: BTC,ETH,SOL"),
    vs_currency: str = Query(default="usd")
):
    """Obtém preços de múltiplos ativos."""
    client = get_coingecko_client()
    symbol_list = [s.strip().upper() for s in symbols.split(",")]
    
    # Map to CoinGecko IDs
    symbol_map = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "SOL": "solana",
        "ADA": "cardano",
        "DOT": "polkadot",
        "XRP": "ripple",
        "DOGE": "dogecoin",
        "LTC": "litecoin"
    }
    ids = [symbol_map.get(s, s.lower()) for s in symbol_list]
    
    try:
        data = await client.get_price(
            ids=ids,
            vs_currencies=[vs_currency],
            include_24hr_change=True,
            include_24hr_vol=True,
            include_market_cap=True
        )
        
        prices = {}
        for symbol, coin_id in zip(symbol_list, ids):
            coin_data = data.get(coin_id, {})
            prices[symbol] = PriceResponse(
                symbol=symbol,
                price=coin_data.get(vs_currency, 0),
                change_24h=coin_data.get(f"{vs_currency}_24h_change"),
                volume_24h=coin_data.get(f"{vs_currency}_24h_vol"),
                market_cap=coin_data.get(f"{vs_currency}_market_cap"),
                timestamp=datetime.now(timezone.utc)
            )
        
        return MultiPriceResponse(prices=prices)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erro ao obter preços: {str(e)}"
        )


@router.get("/history/{symbol}", response_model=PriceHistoryResponse)
async def get_price_history(
    symbol: str,
    days: int = Query(default=30, le=365),
    vs_currency: str = Query(default="usd")
):
    """Obtém histórico de preço."""
    client = get_coingecko_client()
    
    symbol_map = {
        "BTC": "bitcoin",
        "ETH": "ethereum",
        "SOL": "solana"
    }
    coin_id = symbol_map.get(symbol.upper(), symbol.lower())
    
    try:
        data = await client.get_coin_market_chart(
            id=coin_id,
            vs_currency=vs_currency,
            days=days
        )
        
        return PriceHistoryResponse(
            symbol=symbol.upper(),
            prices=data.get("prices", []),
            volumes=data.get("total_volumes", []),
            market_caps=data.get("market_caps", [])
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erro ao obter histórico: {str(e)}"
        )


@router.get("/regime/{symbol}", response_model=MarketRegimeResponse)
async def get_market_regime(
    symbol: str,
    days: int = Query(default=60)
):
    """Detecta regime de mercado atual."""
    client = get_coingecko_client()
    
    symbol_map = {"BTC": "bitcoin", "ETH": "ethereum", "SOL": "solana"}
    coin_id = symbol_map.get(symbol.upper(), symbol.lower())
    
    try:
        # Get historical data
        data = await client.get_coin_market_chart(
            id=coin_id,
            vs_currency="usd",
            days=days
        )
        
        prices = [p[1] for p in data.get("prices", [])]
        if len(prices) < 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Dados insuficientes. São necessários pelo menos 50 pontos de dados."
            )
        
        # Create mock highs/lows for simplicity
        highs = [p * 1.02 for p in prices]
        lows = [p * 0.98 for p in prices]
        volumes = [v[1] for v in data.get("total_volumes", [])]
        
        # Detect regime
        result = regime_detection_engine.detect_regime(
            symbol=symbol.upper(),
            highs=highs,
            lows=lows,
            closes=prices,
            volumes=volumes
        )
        
        return MarketRegimeResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erro ao detectar regime: {str(e)}"
        )


@router.get("/setup-recommendations/{symbol}", response_model=SetupRecommendationResponse)
async def get_setup_recommendations(
    symbol: str,
    days: int = Query(default=60)
):
    """Obtém recomendações de setup para um símbolo."""
    client = get_coingecko_client()
    
    symbol_map = {"BTC": "bitcoin", "ETH": "ethereum", "SOL": "solana"}
    coin_id = symbol_map.get(symbol.upper(), symbol.lower())
    
    try:
        data = await client.get_coin_market_chart(
            id=coin_id,
            vs_currency="usd",
            days=days
        )
        
        prices = [p[1] for p in data.get("prices", [])]
        if len(prices) < 50:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Dados insuficientes para análise"
            )
        
        highs = [p * 1.02 for p in prices]
        lows = [p * 0.98 for p in prices]
        volumes = [v[1] for v in data.get("total_volumes", [])]
        
        # Get current regime
        regime_result = regime_detection_engine.detect_regime(
            symbol.upper(), highs, lows, prices, volumes
        )
        current_regime = regime_result.get("regime_type", "unknown")
        
        # Get setup candidates
        candidates = setup_recommendation_engine.get_all_candidates(
            symbol.upper(), prices, highs, lows, volumes
        )
        
        return SetupRecommendationResponse(
            symbol=symbol.upper(),
            current_regime=current_regime,
            candidates=[{
                "name": c.name,
                "symbol": c.symbol,
                "direction": c.direction,
                "confidence": c.confidence,
                "entry_price": c.entry_price,
                "stop_loss": c.stop_loss,
                "take_profit": c.take_profit,
                "risk_reward_ratio": c.risk_reward_ratio,
                "regime_suitability": c.regime_suitability,
                "reasons": c.reasons,
                "risks": c.risks,
                "timestamp": c.timestamp.isoformat()
            } for c in candidates],
            generated_at=datetime.now(timezone.utc)
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Erro ao gerar recomendações: {str(e)}"
        )
