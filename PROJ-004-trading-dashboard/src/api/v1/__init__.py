from src.api.v1.auth import router as auth_router
from src.api.v1.trades import router as trades_router
from src.api.v1.market import router as market_router
from src.api.v1.portfolio import router as portfolio_router
from src.api.v1.analysis import router as analysis_router

__all__ = [
    "auth_router", "trades_router", "market_router", 
    "portfolio_router", "analysis_router"
]
