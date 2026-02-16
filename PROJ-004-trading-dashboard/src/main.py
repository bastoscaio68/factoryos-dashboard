from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.core.database import init_db, close_db
from src.api.v1 import (
    auth_router, 
    trades_router, 
    market_router, 
    portfolio_router, 
    analysis_router
)
from src.api.websocket import manager


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia ciclo de vida da aplicação."""
    # Startup
    await init_db()
    yield
    # Shutdown
    await close_db()


app = FastAPI(
    title=settings.APP_NAME,
    description="Trading Dashboard API - Análise de mercado, detecção de regimes e recomendações de setup",
    version="1.0.0",
    lifespan=lifespan
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
app.include_router(trades_router, prefix=settings.API_V1_PREFIX)
app.include_router(market_router, prefix=settings.API_V1_PREFIX)
app.include_router(portfolio_router, prefix=settings.API_V1_PREFIX)
app.include_router(analysis_router, prefix=settings.API_V1_PREFIX)


@app.get("/")
async def root():
    """Endpoint raiz."""
    return {
        "name": settings.APP_NAME,
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Verificação de saúde."""
    return {"status": "healthy"}


# WebSocket endpoints
from fastapi import WebSocket, Query


@app.websocket("/ws/market")
async def websocket_market(websocket: WebSocket, symbol: str = None):
    """WebSocket para dados de mercado em tempo real."""
    await manager.connect(websocket, "market")
    try:
        await websocket.send_json({
            "type": "connected",
            "channel": "market",
            "symbol": symbol
        })
        while True:
            await websocket.receive_text()
    except Exception:
        manager.disconnect(websocket, "market")


@app.websocket("/ws/portfolio")
async def websocket_portfolio(websocket: WebSocket, user_id: int = None):
    """WebSocket para atualizações de portfólio."""
    await manager.connect(websocket, "portfolio")
    try:
        await websocket.send_json({
            "type": "connected",
            "channel": "portfolio",
            "user_id": user_id
        })
        while True:
            await websocket.receive_text()
    except Exception:
        manager.disconnect(websocket, "portfolio")


@app.websocket("/ws/alerts")
async def websocket_alerts(websocket: WebSocket, user_id: int = None):
    """WebSocket para alertas."""
    await manager.connect(websocket, "alerts")
    try:
        await websocket.send_json({
            "type": "connected",
            "channel": "alerts",
            "user_id": user_id
        })
        while True:
            await websocket.receive_text()
    except Exception:
        manager.disconnect(websocket, "alerts")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
