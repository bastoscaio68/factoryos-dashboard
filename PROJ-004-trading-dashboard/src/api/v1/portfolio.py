from typing import List, Optional
from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload

from src.core.database import get_db
from src.models import Trade, PortfolioHistory, TradeStatus, User
from src.schemas import PortfolioResponse, PortfolioHistoryResponse

router = APIRouter(prefix="/portfolio", tags=["Portfolio"])


async def get_current_user(
    token: str,
    db: AsyncSession
) -> User:
    """Dependency para obter usuário atual."""
    from src.core.security import decode_access_token
    
    payload = decode_access_token(token)
    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido"
        )
    
    result = await db.execute(select(User).where(User.id == int(payload.get("sub"))))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuário não encontrado"
        )
    
    return user


@router.get("", response_model=PortfolioResponse)
async def get_portfolio(
    token: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Obtém portfólio atual do usuário."""
    user = await get_current_user(token, db)
    
    # Get all open trades
    result = await db.execute(
        select(Trade).where(
            Trade.user_id == user.id,
            Trade.status == TradeStatus.OPEN
        )
    )
    open_trades = result.scalars().all()
    
    # Calculate portfolio (simplified - would need real prices)
    holdings = []
    total_value = 0
    total_cost = 0
    
    for trade in open_trades:
        # Simulated current price (in real app, fetch from API)
        current_price = trade.entry_price * 1.05 if trade.side.value == "long" else trade.entry_price * 0.95
        value = current_price * trade.quantity
        cost = trade.entry_price * trade.quantity
        
        holdings.append({
            "symbol": trade.symbol,
            "quantity": trade.quantity,
            "avg_price": trade.entry_price,
            "current_price": current_price,
            "value": value,
            "pnl": value - cost,
            "pnl_percent": ((value - cost) / cost) * 100 if cost > 0 else 0
        })
        
        total_value += value
        total_cost += cost
    
    total_pnl = total_value - total_cost
    total_pnl_percent = (total_pnl / total_cost * 100) if total_cost > 0 else 0
    
    return PortfolioResponse(
        total_value=total_value,
        total_pnl=total_pnl,
        total_pnl_percent=total_pnl_percent,
        holdings=holdings,
        timestamp=datetime.now(timezone.utc)
    )


@router.get("/history", response_model=PortfolioHistoryResponse)
async def get_portfolio_history(
    days: int = Query(default=30, le=365),
    token: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Obtém histórico do portfólio."""
    user = await get_current_user(token, db)
    
    # Get portfolio history records
    result = await db.execute(
        select(PortfolioHistory)
        .where(PortfolioHistory.user_id == user.id)
        .order_by(PortfolioHistory.timestamp.desc())
        .limit(days)
    )
    history_records = result.scalars().all()
    
    history = [
        {
            "total_value": r.total_value,
            "pnl": r.pnl_total,
            "timestamp": r.timestamp.isoformat()
        }
        for r in history_records
    ]
    
    return PortfolioHistoryResponse(history=history)


@router.post("/snapshot")
async def create_portfolio_snapshot(
    token: String = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Cria snapshot do portfólio atual."""
    user = await get_current_user(token, db)
    
    # Get current holdings value (simplified)
    result = await db.execute(
        select(Trade).where(
            Trade.user_id == user.id,
            Trade.status == TradeStatus.OPEN
        )
    )
    open_trades = result.scalars().all()
    
    total_value = sum(
        t.entry_price * t.quantity * (1.05 if t.side.value == "long" else 0.95)
        for t in open_trades
    )
    
    holdings = {t.symbol: t.quantity for t in open_trades}
    
    snapshot = PortfolioHistory(
        user_id=user.id,
        total_value=total_value,
        holdings=holdings,
        pnl_day=0,  # Would calculate from previous snapshot
        pnl_total=total_value - sum(t.entry_price * t.quantity for t in open_trades),
        timestamp=datetime.now(timezone.utc)
    )
    
    db.add(snapshot)
    await db.commit()
    
    return {"message": "Snapshot criado com sucesso", "id": snapshot.id}
