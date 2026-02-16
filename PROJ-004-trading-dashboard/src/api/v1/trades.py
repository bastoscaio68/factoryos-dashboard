from datetime import datetime, timezone
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.core.database import get_db
from src.core.security import decode_access_token
from src.models import Trade, TradeStatus, TradeSide, User
from src.schemas import TradeCreate, TradeUpdate, TradeResponse, TradeListResponse

router = APIRouter(prefix="/trades", tags=["Trades"])


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


@router.get("", response_model=TradeListResponse)
async def list_trades(
    symbol: Optional[str] = None,
    status: Optional[str] = None,
    limit: int = Query(default=50, le=100),
    offset: int = 0,
    token: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Lista trades do usuário."""
    user = await get_current_user(token, db)
    
    # Construir query
    query = select(Trade).where(Trade.user_id == user.id)
    
    if symbol:
        query = query.where(Trade.symbol == symbol.upper())
    if status:
        query = query.where(Trade.status == status)
    
    # Contar total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    
    # Paginar
    query = query.order_by(Trade.created_at.desc())
    query = query.offset(offset).limit(limit)
    
    result = await db.execute(query)
    trades = result.scalars().all()
    
    return TradeListResponse(
        total=total,
        trades=[TradeResponse.model_validate(t) for t in trades]
    )


@router.get("/{trade_id}", response_model=TradeResponse)
async def get_trade(
    trade_id: int,
    token: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Obtém detalhes de um trade."""
    user = await get_current_user(token, db)
    
    result = await db.execute(
        select(Trade).where(Trade.id == trade_id, Trade.user_id == user.id)
    )
    trade = result.scalar_one_or_none()
    
    if not trade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trade não encontrado"
        )
    
    return trade


@router.post("", response_model=TradeResponse, status_code=status.HTTP_201_CREATED)
async def create_trade(
    trade_data: TradeCreate,
    token: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Cria novo trade."""
    user = await get_current_user(token, db)
    
    trade = Trade(
        user_id=user.id,
        symbol=trade_data.symbol.upper(),
        entry_price=trade_data.entry_price,
        quantity=trade_data.quantity,
        side=TradeSide(trade_data.side),
        status=TradeStatus.OPEN,
        entry_time=datetime.now(timezone.utc),
        notes=trade_data.notes
    )
    
    db.add(trade)
    await db.commit()
    await db.refresh(trade)
    
    return trade


@router.put("/{trade_id}", response_model=TradeResponse)
async def update_trade(
    trade_id: int,
    trade_data: TradeUpdate,
    token: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Atualiza um trade."""
    user = await get_current_user(token, db)
    
    result = await db.execute(
        select(Trade).where(Trade.id == trade_id, Trade.user_id == user.id)
    )
    trade = result.scalar_one_or_none()
    
    if not trade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trade não encontrado"
        )
    
    # Atualizar campos
    if trade_data.exit_price is not None:
        trade.exit_price = trade_data.exit_price
        # Calcular P&L
        if trade.side == TradeSide.LONG:
            trade.pnl = (trade_data.exit_price - trade.entry_price) * trade.quantity
        else:
            trade.pnl = (trade.entry_price - trade_data.exit_price) * trade.quantity
        trade.exit_time = datetime.now(timezone.utc)
    
    if trade_data.status:
        trade.status = TradeStatus(trade_data.status)
        if trade_data.status == "closed":
            trade.exit_time = datetime.now(timezone.utc)
    
    if trade_data.notes is not None:
        trade.notes = trade_data.notes
    
    await db.commit()
    await db.refresh(trade)
    
    return trade


@router.delete("/{trade_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_trade(
    trade_id: int,
    token: str = Query(...),
    db: AsyncSession = Depends(get_db)
):
    """Deleta um trade."""
    user = await get_current_user(token, db)
    
    result = await db.execute(
        select(Trade).where(Trade.id == trade_id, Trade.user_id == user.id)
    )
    trade = result.scalar_one_or_none()
    
    if not trade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Trade não encontrado"
        )
    
    await db.delete(trade)
    await db.commit()
