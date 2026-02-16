from typing import Dict, Set, Optional
from fastapi import WebSocket, WebSocketDisconnect
import asyncio
import json
from datetime import datetime, timezone


class ConnectionManager:
    """Gerencia conexões WebSocket."""
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {
            "market": set(),
            "portfolio": set(),
            "alerts": set()
        }
    
    async def connect(
        self, 
        websocket: WebSocket, 
        channel: str
    ):
        """Aceita nova conexão WebSocket."""
        await websocket.accept()
        if channel not in self.active_connections:
            self.active_connections[channel] = set()
        self.active_connections[channel].add(websocket)
    
    def disconnect(self, websocket: WebSocket, channel: str):
        """Remove conexão WebSocket."""
        if channel in self.active_connections:
            self.active_connections[channel].discard(websocket)
    
    async def broadcast(self, channel: str, message: dict):
        """Envia mensagem para todas as conexões de um canal."""
        if channel not in self.active_connections:
            return
        
        disconnected = []
        for connection in self.active_connections[channel]:
            try:
                await connection.send_json(message)
            except WebSocketDisconnect:
                disconnected.append(connection)
        
        # Remove conexões desconectadas
        for conn in disconnected:
            self.disconnect(conn, channel)
    
    async def broadcast_price_update(self, symbol: str, price_data: dict):
        """Broadcast atualização de preço."""
        message = {
            "type": "price_update",
            "symbol": symbol,
            "data": price_data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await self.broadcast("market", message)
    
    async def broadcast_portfolio_update(self, user_id: int, portfolio_data: dict):
        """Broadcast atualização de portfólio."""
        message = {
            "type": "portfolio_update",
            "user_id": user_id,
            "data": portfolio_data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await self.broadcast("portfolio", message)
    
    async def broadcast_alert(self, alert_data: dict):
        """Broadcast alerta."""
        message = {
            "type": "alert",
            "data": alert_data,
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
        await self.broadcast("alerts", message)


# Singleton instance
manager = ConnectionManager()


async def websocket_market_endpoint(websocket: WebSocket, symbol: str = None):
    """Endpoint WebSocket para preços em tempo real."""
    await manager.connect(websocket, "market")
    try:
        # Send initial data
        await websocket.send_json({
            "type": "connected",
            "channel": "market",
            "symbol": symbol,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        # Keep connection alive
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, "market")


async def websocket_portfolio_endpoint(websocket: WebSocket, user_id: int = None):
    """Endpoint WebSocket para atualizações de portfólio."""
    await manager.connect(websocket, "portfolio")
    try:
        await websocket.send_json({
            "type": "connected",
            "channel": "portfolio",
            "user_id": user_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, "portfolio")


async def websocket_alerts_endpoint(websocket: WebSocket, user_id: int = None):
    """Endpoint WebSocket para alertas."""
    await manager.connect(websocket, "alerts")
    try:
        await websocket.send_json({
            "type": "connected",
            "channel": "alerts",
            "user_id": user_id,
            "timestamp": datetime.now(timezone.utc).isoformat()
        })
        
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, "alerts")
