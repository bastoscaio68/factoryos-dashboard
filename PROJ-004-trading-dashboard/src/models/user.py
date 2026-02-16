from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float, Boolean, JSON
from sqlalchemy.sql import func
from src.core.database import Base


class User(Base):
    """Model de Usuário."""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    
    # Relationships
    trades = relationship("Trade", back_populates="user")
    performance_metrics = relationship("PerformanceMetric", back_populates="user")
    portfolio_history = relationship("PortfolioHistory", back_populates="user")
