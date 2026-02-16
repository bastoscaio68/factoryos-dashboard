from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel


# Market Schemas
class PriceResponse(BaseModel):
    symbol: str
    price: float
    change_24h: Optional[float]
    volume_24h: Optional[float]
    market_cap: Optional[float]
    timestamp: datetime


class PriceHistoryResponse(BaseModel):
    symbol: str
    prices: List[List[float]]  # [timestamp, price]
    volumes: List[List[float]]
    market_caps: List[List[float]]


class MultiPriceResponse(BaseModel):
    prices: Dict[str, PriceResponse]


# Market Regime Schemas
class MarketRegimeFeatures(BaseModel):
    atr: float
    adx: float
    plus_di: float
    minus_di: float
    volatility: float
    fast_ma: float
    slow_ma: float
    vol_ratio: float
    trend_strength: float
    is_trending: bool


class MarketRegimeResponse(BaseModel):
    symbol: str
    regime_type: str
    confidence: float
    features: MarketRegimeFeatures
    timestamp: datetime
    
    class Config:
        from_attributes = True


# Setup Recommendation Schemas
class SetupCandidateResponse(BaseModel):
    name: str
    symbol: str
    direction: str
    confidence: float
    entry_price: float
    stop_loss: float
    take_profit: float
    risk_reward_ratio: float
    regime_suitability: float
    reasons: List[str]
    risks: List[str]
    timestamp: datetime


class SetupRecommendationResponse(BaseModel):
    symbol: str
    current_regime: str
    candidates: List[SetupCandidateResponse]
    generated_at: datetime


# Performance Schemas
class PerformanceMetricResponse(BaseModel):
    win_rate: Optional[float]
    profit_factor: Optional[float]
    expectancy: Optional[float]
    avg_win: Optional[float]
    avg_loss: Optional[float]
    max_drawdown: Optional[float]
    period: str
    period_start: Optional[datetime]
    period_end: Optional[datetime]


# Portfolio Schemas
class PortfolioHolding(BaseModel):
    symbol: str
    quantity: float
    avg_price: float
    current_price: float
    value: float
    pnl: float
    pnl_percent: float


class PortfolioResponse(BaseModel):
    total_value: float
    total_pnl: float
    total_pnl_percent: float
    holdings: List[PortfolioHolding]
    timestamp: datetime


class PortfolioHistoryResponse(BaseModel):
    history: List[dict]
