import httpx
from typing import List, Dict, Optional
from src.core.config import settings


class CoinGeckoClient:
    """Cliente async para CoinGecko API."""
    
    def __init__(self):
        self.base_url = settings.COINGECKO_API_URL
        self.client = httpx.AsyncClient(timeout=30.0)
    
    async def close(self):
        """Fecha o cliente HTTP."""
        await self.client.aclose()
    
    async def get_price(
        self, 
        ids: List[str], 
        vs_currencies: List[str] = ["usd"],
        include_24hr_change: bool = True,
        include_24hr_vol: bool = True,
        include_market_cap: bool = True
    ) -> Dict[str, Dict]:
        """Obtém preço atual de uma ou mais moedas."""
        params = {
            "ids": ",".join(ids),
            "vs_currencies": ",".join(vs_currencies),
            "include_24hr_change": include_24hr_change,
            "include_24hr_vol": include_24hr_vol,
            "include_market_cap": include_market_cap
        }
        response = await self.client.get(f"{self.base_url}/simple/price", params=params)
        response.raise_for_status()
        return response.json()
    
    async def get_coin_market_chart(
        self,
        id: str,
        vs_currency: str = "usd",
        days: int = 30,
        interval: str = "daily"
    ) -> Dict:
        """Obtém histórico de preço de uma moeda."""
        params = {
            "vs_currency": vs_currency,
            "days": days,
            "interval": interval
        }
        response = await self.client.get(
            f"{self.base_url}/coins/{id}/market_chart", 
            params=params
        )
        response.raise_for_status()
        return response.json()
    
    async def get_coin_market_data(self, id: str) -> Dict:
        """Obtém dados de mercado detalhados de uma moeda."""
        response = await self.client.get(
            f"{self.base_url}/coins/{id}",
            params={
                "localization": False,
                "tickers": False,
                "community_data": False,
                "developer_data": False,
                "sparkline": True
            }
        )
        response.raise_for_status()
        return response.json()
    
    async def search_coins(self, query: str) -> List[Dict]:
        """Busca moedas por nome ou símbolo."""
        response = await self.client.get(
            f"{self.base_url}/search",
            params={"query": query}
        )
        response.raise_for_status()
        return response.json().get("coins", [])[:10]
    
    async def get_global_data(self) -> Dict:
        """Obtém dados globais do mercado."""
        response = await self.client.get(f"{self.base_url}/global")
        response.raise_for_status()
        return response.json().get("data", {})


# Singleton instance
_coingecko_client: Optional[CoinGeckoClient] = None


def get_coingecko_client() -> CoinGeckoClient:
    """Dependency para obter cliente CoinGecko."""
    global _coingecko_client
    if _coingecko_client is None:
        _coingecko_client = CoinGeckoClient()
    return _coingecko_client
