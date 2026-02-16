from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


# Auth Schemas
class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


# Trade Schemas
class TradeCreate(BaseModel):
    symbol: str
    entry_price: float
    quantity: float
    side: str  # long or short
    notes: Optional[str] = None


class TradeUpdate(BaseModel):
    exit_price: Optional[float] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class TradeResponse(BaseModel):
    id: int
    user_id: int
    symbol: str
    entry_price: float
    exit_price: Optional[float]
    quantity: float
    side: str
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
