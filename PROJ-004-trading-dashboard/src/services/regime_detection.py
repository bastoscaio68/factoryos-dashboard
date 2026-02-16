import numpy as np
from typing import Dict, List, Tuple
from datetime import datetime, timezone
from src.models.market_regime import MarketRegimeType


class RegimeDetectionEngine:
    """Engine de detecção de regime de mercado."""
    
    def __init__(self):
        self.atr_period = 14
        self.adx_period = 14
        self.adx_threshold = 25
        self.vol_sma_period = 20
    
    def calculate_atr(self, highs: List[float], lows: List[float], closes: List[float]) -> float:
        """Calcula Average True Range."""
        if len(closes) < self.atr_period + 1:
            return 0.0
        
        true_ranges = []
        for i in range(1, len(closes)):
            tr = max(
                highs[i] - lows[i],
                abs(highs[i] - closes[i-1]),
                abs(lows[i] - closes[i-1])
            )
            true_ranges.append(tr)
        
        return float(np.mean(true_ranges[-self.atr_period:]))
    
    def calculate_adx(self, highs: List[float], lows: List[float], closes: List[float]) -> Tuple[float, float, float]:
        """
        Calcula Average Directional Index.
        Returns: (adx, plus_di, minus_di)
        """
        if len(closes) < self.adx_period + 1:
            return 0.0, 0.0, 0.0
        
        plus_dms = []
        minus_dms = []
        true_ranges = []
        
        for i in range(1, len(closes)):
            high_diff = highs[i] - highs[i-1]
            low_diff = lows[i-1] - lows[i]
            
            plus_dm = high_diff if high_diff > low_diff and high_diff > 0 else 0
            minus_dm = low_diff if low_diff > high_diff and low_diff > 0 else 0
            
            plus_dms.append(plus_dm)
            minus_dms.append(minus_dm)
            
            tr = max(
                highs[i] - lows[i],
                abs(highs[i] - closes[i-1]),
                abs(lows[i] - closes[i-1])
            )
            true_ranges.append(tr)
        
        plus_di = 100 * np.mean(plus_dms[-self.adx_period:]) / np.mean(true_ranges[-self.adx_period:])
        minus_di = 100 * np.mean(minus_dms[-self.adx_period:]) / np.mean(true_ranges[-self.adx_period:])
        
        dx = abs(plus_di - minus_di) / (plus_di + minus_di) * 100 if (plus_di + minus_di) > 0 else 0
        
        adx = np.mean(dx) if isinstance(dx, (list, np.ndarray)) else dx
        
        return float(adx), float(plus_di), float(minus_di)
    
    def calculate_volatility(self, closes: List[float]) -> float:
        """Calcula volatilidade (desvio padrão)."""
        if len(closes) < 2:
            return 0.0
        returns = np.diff(closes) / closes[:-1]
        return float(np.std(returns) * np.sqrt(365))  # Anualizada
    
    def calculate_moving_averages(self, closes: List[float], fast: int = 20, slow: int = 50) -> Tuple[float, float]:
        """Calcula médias móveis."""
        if len(closes) < slow:
            return float(np.mean(closes[-fast:])), float(np.mean(closes[-slow:]))
        
        fast_ma = float(np.mean(closes[-fast:]))
        slow_ma = float(np.mean(closes[-slow:]))
        
        return fast_ma, slow_ma
    
    def detect_regime(
        self,
        symbol: str,
        highs: List[float],
        lows: List[float],
        closes: List[float],
        volumes: List[float] = None
    ) -> Dict:
        """
        Detecta o regime de mercado atual.
        
        Returns:
            Dict com regime_type, confidence, e features
        """
        if len(closes) < 50:
            return {
                "symbol": symbol,
                "regime_type": MarketRegimeType.SIDEWAYS.value,
                "confidence": 0.5,
                "features": {"error": "Dados insuficientes"}
            }
        
        # Cálculo de indicadores
        atr = self.calculate_atr(highs, lows, closes)
        adx, plus_di, minus_di = self.calculate_adx(highs, lows, closes)
        volatility = self.calculate_volatility(closes)
        fast_ma, slow_ma = self.calculate_moving_averages(closes)
        
        # Análise de tendência
        trend_strength = abs(plus_di - minus_di)
        is_trending = adx > self.adx_threshold
        
        # Análise de volatilidade
        avg_vol = np.mean(volumes) if volumes else 0
        current_vol = np.std(np.diff(closes[-30:]) / closes[-31:-1]) if len(closes) > 31 else 0
        vol_ratio = current_vol / avg_vol if avg_vol > 0 else 1
        
        # Determinação do regime
        if is_trending:
            if plus_di > minus_di:
                regime = MarketRegimeType.BULL_TREND
            else:
                regime = MarketRegimeType.BEAR_TREND
            confidence = min(adx / 50, 1.0)
        else:
            if vol_ratio > 1.5:
                regime = MarketRegimeType.HIGH_VOLATILITY
            else:
                regime = MarketRegimeType.SIDEWAYS
            confidence = 0.6
        
        features = {
            "atr": atr,
            "adx": adx,
            "plus_di": plus_di,
            "minus_di": minus_di,
            "volatility": volatility,
            "fast_ma": fast_ma,
            "slow_ma": slow_ma,
            "vol_ratio": vol_ratio,
            "trend_strength": trend_strength,
            "is_trending": is_trending
        }
        
        return {
            "symbol": symbol,
            "regime_type": regime.value,
            "confidence": confidence,
            "features": features,
            "timestamp": datetime.now(timezone.utc)
        }
    
    def get_recommended_strategy(self, regime: str) -> Dict:
        """Retorna estratégia recomendada para cada regime."""
        strategies = {
            MarketRegimeType.BULL_TREND.value: {
                "strategy": "Trend Following",
                "setup_preference": ["breakout", "moving_average_crossover"],
                "risk_level": "moderate",
                "description": "Acompanhar tendências de alta com entradas favoráveis"
            },
            MarketRegimeType.BEAR_TREND.value: {
                "strategy": "Short Selling",
                "setup_preference": ["resistance_rejection", "bearish_breakdown"],
                "risk_level": "high",
                "description": "Buscar oportunidades de venda short"
            },
            MarketRegimeType.SIDEWAYS.value: {
                "strategy": "Range Trading",
                "setup_preference": ["support_resistance", "mean_reversion"],
                "risk_level": "low",
                "description": "Operar entre suportes e resistências"
            },
            MarketRegimeType.HIGH_VOLATILITY.value: {
                "strategy": "Volatility Breakout",
                "setup_preference": ["volatility_expansion", "gap_trading"],
                "risk_level": "high",
                "description": "Explodir movimentos de alta volatilidade"
            },
            MarketRegimeType.LOW_VOLATILITY.value: {
                "strategy": "Waiting Mode",
                "setup_preference": [],
                "risk_level": "low",
                "description": "Aguardar configurações de maior probabilidade"
            }
        }
        return strategies.get(regime, {"strategy": "Unknown", "setup_preference": []})


regime_detection_engine = RegimeDetectionEngine()
