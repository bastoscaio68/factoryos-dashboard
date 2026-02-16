from typing import Optional
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.core.database import get_db
from src.core.security import decode_access_token
from src.models import Trade, PerformanceMetric, TradeStatus, User
from src.schemas import PerformanceMetricResponse

router = APIRouter(prefix="/analysis", tags=["Analysis"])


async def get_current_user(
    token: str,
    db: AsyncSession
) -> User:
    """Dependency para obter usuário atual."""
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


@router.get("/performance", response_model=PerformanceMetricResponse)
async def get_performance(
    period: str = Query(default="all", regex="^(all|weekly|monthly|daily)$"),
    token: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Obtém métricas de performance."""
    user = await get_current_user(token, db)
    
    # Get closed trades
    query = select(Trade).where(
        Trade.user_id == user.id,
        Trade.status == TradeStatus.CLOSED
    )
    
    if period != "all":
        from datetime import datetime, timedelta
        if period == "daily":
            start_date = datetime.now(timezone.utc) - timedelta(days=1)
        elif period == "weekly":
            start_date = datetime.now(timezone.utc) - timedelta(weeks=1)
        elif period == "monthly":
            start_date = datetime.now(timezone.utc) - timedelta(days=30)
        query = query.where(Trade.exit_time >= start_date)
    
    result = await db.execute(query)
    trades = result.scalars().all()
    
    if not trades:
        return PerformanceMetricResponse(
            win_rate=0,
            profit_factor=0,
            expectancy=0,
            avg_win=0,
            avg_loss=0,
            max_drawdown=0,
            period=period,
            period_start=None,
            period_end=None
        )
    
    # Calculate metrics
    winning_trades = [t for t in trades if t.pnl and t.pnl > 0]
    losing_trades = [t for t in trades if t.pnl and t.pnl <= 0]
    
    total_trades = len(trades)
    wins = len(winning_trades)
    losses = len(losing_trades)
    
    # Win Rate
    win_rate = (wins / total_trades * 100) if total_trades > 0 else 0
    
    # Average Win/Loss
    avg_win = sum(t.pnl for t in winning_trades) / wins if wins > 0 else 0
    avg_loss = abs(sum(t.pnl for t in losing_trades) / losses) if losses > 0 else 0
    
    # Profit Factor
    gross_profit = sum(t.pnl for t in winning_trades)
    gross_loss = abs(sum(t.pnl for t in losing_trades))
    profit_factor = gross_profit / gross_loss if gross_loss > 0 else float('inf')
    
    # Expectancy
    expectancy = (win_rate/100 * avg_win) - ((1 - win_rate/100) * avg_loss)
    
    # Max Drawdown (simplified)
    running_pnl = 0
    max_drawdown = 0
    peak = 0
    
    sorted_trades = sorted(trades, key=lambda t: t.exit_time if t.exit_time else datetime.min)
    for t in sorted_trades:
        if t.pnl:
            running_pnl += t.pnl
            if running_pnl > peak:
                peak = running_pnl
            drawdown = peak - running_pnl
            if drawdown > max_drawdown:
                max_drawdown = drawdown
    
    return PerformanceMetricResponse(
        win_rate=round(win_rate, 2),
        profit_factor=round(profit_factor, 2) if profit_factor != float('inf') else 999,
        expectancy=round(expectancy, 4),
        avg_win=round(avg_win, 2),
        avg_loss=round(avg_loss, 2),
        max_drawdown=round(max_drawdown, 2),
        period=period,
        period_start=sorted_trades[0].exit_time if sorted_trades else None,
        period_end=sorted_trades[-1].exit_time if sorted_trades else None
    )


@router.get("/summary")
async def get_summary(
    token: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Obtém resumo geral da performance."""
    user = await get_current_user(token, db)
    
    # Get all trades
    result = await db.execute(
        select(Trade).where(Trade.user_id == user.id)
    )
    all_trades = result.scalars().all()
    
    open_trades = [t for t in all_trades if t.status == TradeStatus.OPEN]
    closed_trades = [t for t in all_trades if t.status == TradeStatus.CLOSED]
    
    total_closed = len(closed_trades)
    wins = len([t for t in closed_trades if t.pnl and t.pnl > 0])
    losses = total_closed - wins
    
    total_pnl = sum(t.pnl or 0 for t in closed_trades)
    win_rate = (wins / total_closed * 100) if total_closed > 0 else 0
    
    return {
        "total_trades": len(all_trades),
        "open_trades": len(open_trades),
        "closed_trades": total_closed,
        "wins": wins,
        "losses": losses,
        "win_rate": round(win_rate, 2),
        "total_pnl": round(total_pnl, 2),
        "symbols_traded": list(set(t.symbol for t in all_trades))
    }
