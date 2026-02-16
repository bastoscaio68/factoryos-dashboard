from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.core.database import Base


class PortfolioHistory(Base):
    """Model de Histórico do Portfólio."""
    __tablename__ = "portfolio_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    total_value = Column(Float, nullable=False)
    holdings = Column(JSON, nullable=True)  # {symbol: quantity, ...}
    pnl_day = Column(Float, nullable=True)
    pnl_total = Column(Float, nullable=True)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="portfolio_history")
