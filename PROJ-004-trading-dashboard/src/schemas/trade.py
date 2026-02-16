from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel


class TradeBase(BaseModel):
    symbol: str
    entry_price: float
    quantity: float
    side: str


class TradeCreate(TradeBase):
    notes: Optional[str] = None


class TradeUpdate(BaseModel):
    exit_price: Optional[float] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class TradeResponse(TradeBase):
    id: int
    user_id: int
    exit_price: Optional[float]
    status: str
    pnl: Optional[float]
    notes: Optional[str]
    entry_time: Optional[datetime]
    exit_time: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True


class TradeListResponse(BaseModel):
    total: int
    trades: List[TradeResponse]
