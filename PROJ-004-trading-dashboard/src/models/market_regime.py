from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON
from sqlalchemy.sql import func
from src.core.database import Base
import enum


class MarketRegimeType(str, enum.Enum):
    BULL_TREND = "bull_trend"
    BEAR_TREND = "bear_trend"
    SIDEWAYS = "sideways"
    HIGH_VOLATILITY = "high_volatility"
    LOW_VOLATILITY = "low_volatility"


class MarketRegime(Base):
    """Model de Regime de Mercado."""
    __tablename__ = "market_regimes"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False, index=True)
    regime_type = Column(String(30), nullable=False)
    confidence = Column(Float, nullable=False)  # 0-1
    start_time = Column(DateTime(timezone=True), nullable=False)
    end_time = Column(DateTime(timezone=True), nullable=True)
    features = Column(JSON, nullable=True)  # ATR, ADX, volumes, etc.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
