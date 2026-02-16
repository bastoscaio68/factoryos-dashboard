from typing import Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime, timezone
import numpy as np


@dataclass
class SetupCandidate:
    """Candidato de setup para recomendação."""
    name: str
    symbol: str
    direction: str  # long or short
    confidence: float
    entry_price: float
    stop_loss: float
    take_profit: float
    risk_reward_ratio: float
    regime_suitability: float
    reasons: List[str]
    risks: List[str]
    timestamp: datetime


class SetupRecommendationEngine:
    """Engine de recomendação de setup de trading."""
    
    def __init__(self):
        self.atr_period = 14
        self.min_confidence = 0.6
        self.min_risk_reward = 1.5
    
    def calculate_support_resistance(
        self, 
        closes: List[float], 
        window: int = 20
    ) -> Dict:
        """Calcula suportes e resistências."""
        if len(closes) < window:
            return {"support": min(closes), "resistance": max(closes)}
        
        recent = closes[-window:]
        support = min(recent)
        resistance = max(recent)
        
        # Identificar níveis intermediários
        levels = []
        for i in range(1, 5):
            level = support + (resistance - support) * i / 5
            levels.append(round(level, 4))
        
        return {
            "support": support,
            "resistance": resistance,
            "levels": levels
        }
    
    def detect_breakout(
        self,
        symbol: str,
        closes: List[float],
        highs: List[float],
        lows: List[float],
        volume: List[float],
        lookback: int = 20
    ) -> Optional[SetupCandidate]:
        """Detecta padrões de breakout."""
        if len(closes) < lookback:
            return None
        
        recent_high = max(highs[-lookback:-1])
        recent_low = min(lows[-lookback:-1])
        current_close = closes[-1]
        current_vol = volume[-1] if volume else 0
        avg_vol = np.mean(volume[-lookback:]) if volume else 1
        
        reasons = []
        risks = []
        direction = None
        entry_price = None
        
        # Breakout bullish
        if current_close > recent_high:
            direction = "long"
            entry_price = current_close
            
            # Confirmação por volume
            vol_confirmation = current_vol > avg_vol * 1.5
            
            if vol_confirmation:
                reasons.append(f"Breakout de alta com volume ({current_vol/avg_vol:.1f}x média)")
            else:
                reasons.append("Breakout de alta (volume abaixo da média)")
                risks.append("Falta de confirmação de volume")
            
            # Calcular stop e target
            atr = self._calculate_atr(highs, lows, closes)
            stop_loss = recent_low
            take_profit = current_close + (current_close - stop_loss) * 2
            
            confidence = 0.7
            if vol_confirmation:
                confidence += 0.1
            
            return SetupCandidate(
                name="Breakout Bullish",
                symbol=symbol,
                direction=direction,
                confidence=min(confidence, 0.95),
                entry_price=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                risk_reward_ratio=(take_profit - entry_price) / (entry_price - stop_loss),
                regime_suitability=0.8,
                reasons=reasons,
                risks=risks + ["Risco de fakeout", "Reversão possível"],
                timestamp=datetime.now(timezone.utc)
            )
        
        # Breakout bearish
        if current_close < recent_low:
            direction = "short"
            entry_price = current_close
            
            vol_confirmation = current_vol > avg_vol * 1.5
            
            reasons.append("Breakout de baixa detectado")
            if vol_confirmation:
                reasons.append(f"Confirmação por volume ({current_vol/avg_vol:.1f}x média)")
            else:
                risks.append("Falta de confirmação de volume")
            
            atr = self._calculate_atr(highs, lows, closes)
            stop_loss = recent_high
            take_profit = current_close + (stop_loss - current_close) * 2
            
            return SetupCandidate(
                name="Breakout Bearish",
                symbol=symbol,
                direction=direction,
                confidence=0.65 if not vol_confirmation else 0.75,
                entry_price=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                risk_reward_ratio=(entry_price - take_profit) / (stop_loss - entry_price),
                regime_suitability=0.8,
                reasons=reasons,
                risks=risks + ["Risco de fakeout"],
                timestamp=datetime.now(timezone.utc)
            )
        
        return None
    
    def detect_moving_average_crossover(
        self,
        symbol: str,
        closes: List[float],
        fast: int = 9,
        slow: int = 21
    ) -> Optional[SetupCandidate]:
        """Detecta cruzamento de médias móveis."""
        if len(closes) < slow + 5:
            return None
        
        fast_ma = np.mean(closes[-fast:])
        slow_ma = np.mean(closes[-slow:])
        prev_fast_ma = np.mean(closes[-(fast+1):-1])
        prev_slow_ma = np.mean(closes[-(slow+1):-1])
        
        reasons = []
        
        # Golden Cross (bullish)
        if prev_fast_ma <= prev_slow_ma and fast_ma > slow_ma:
            reasons.append(f"Golden Cross: MA{fast} cruzou acima MA{slow}")
            reasons.append(f"MA{fast}={fast_ma:.4f}, MA{slow}={slow_ma:.4f}")
            
            atr = self._calculate_atr_from_closes(closes)
            entry = closes[-1]
            stop = min(closes[-slow:])  # Stop abaixo da mínima do período lento
            
            return SetupCandidate(
                name="Golden Cross",
                symbol=symbol,
                direction="long",
                confidence=0.75,
                entry_price=entry,
                stop_loss=stop,
                take_profit=entry + (entry - stop) * 2,
                risk_reward_ratio=2.0,
                regime_suitability=0.7,
                reasons=reasons,
                risks=["Possível pullback", "Sinal pode atrasar"],
                timestamp=datetime.now(timezone.utc)
            )
        
        # Death Cross (bearish)
        if prev_fast_ma >= prev_slow_ma and fast_ma < slow_ma:
            reasons.append(f"Death Cross: MA{fast} cruzou abaixo MA{slow}")
            
            atr = self._calculate_atr_from_closes(closes)
            entry = closes[-1]
            stop = max(closes[-slow:])
            
            return SetupCandidate(
                name="Death Cross",
                symbol=symbol,
                direction="short",
                confidence=0.70,
                entry_price=entry,
                stop_loss=stop,
                take_profit=entry - (stop - entry) * 2,
                risk_reward_ratio=2.0,
                regime_suitability=0.7,
                reasons=reasons,
                risks=["Possível pullback"],
                timestamp=datetime.now(timezone.utc)
            )
        
        return None
    
    def detect_support_resistance_bounce(
        self,
        symbol: str,
        closes: List[float],
        lows: List[float],
        highs: List[float],
        tolerance: float = 0.02
    ) -> Optional[SetupCandidate]:
        """Detecta rebote em suporte/resistência."""
        if len(closes) < 30:
            return None
        
        support = min(lows[-20:])
        resistance = max(highs[-20:])
        current = closes[-1]
        current_low = lows[-1]
        
        reasons = []
        
        # Bounce no suporte
        if current_low <= support * (1 + tolerance) and current > current_low:
            reasons.append(f"Preço tocando suporte em {support:.4f}")
            reasons.append(f"Distância do suporte: {((current - support) / current * 100):.2f}%")
            
            atr = self._calculate_atr_from_closes(closes)
            
            return SetupCandidate(
                name="Support Bounce",
                symbol=symbol,
                direction="long",
                confidence=0.65,
                entry_price=current,
                stop_loss=support * 0.99,
                take_profit=resistance,
                risk_reward_ratio=(resistance - current) / (current - support * 0.99),
                regime_suitability=0.75,
                reasons=reasons,
                risks=["Suporte pode ser quebrado", "Sinal false"],
                timestamp=datetime.now(timezone.utc)
            )
        
        # Bounce na resistência (reversal)
        if highs[-1] >= resistance * (1 - tolerance) and current < highs[-1]:
            reasons.append(f"Preço tocando resistência em {resistance:.4f}")
            
            return SetupCandidate(
                name="Resistance Rejection",
                symbol=symbol,
                direction="short",
                confidence=0.60,
                entry_price=current,
                stop_loss=resistance * 1.01,
                take_profit=support,
                risk_reward_ratio=(current - support) / (resistance * 1.01 - current),
                regime_suitability=0.70,
                reasons=reasons,
                risks=["Resistência pode ser quebrada"],
                timestamp=datetime.now(timezone.utc)
            )
        
        return None
    
    def get_all_candidates(
        self,
        symbol: str,
        closes: List[float],
        highs: List[float],
        lows: List[float],
        volume: List[float]
    ) -> List[SetupCandidate]:
        """Obtém todos os candidatos de setup para um símbolo."""
        candidates = []
        
        # Breakout
        breakout = self.detect_breakout(symbol, closes, highs, lows, volume)
        if breakout:
            candidates.append(breakout)
        
        # MA Crossover
        ma_crossover = self.detect_moving_average_crossover(symbol, closes)
        if ma_crossover:
            candidates.append(ma_crossover)
        
        # Support/Resistance
        sr = self.detect_support_resistance_bounce(symbol, closes, lows, highs)
        if sr:
            candidates.append(sr)
        
        # Ordenar por confiança
        candidates.sort(key=lambda x: x.confidence, reverse=True)
        
        return candidates
    
    def _calculate_atr(self, highs: List[float], lows: List[float], closes: List[float]) -> float:
        """Calcula ATR."""
        true_ranges = []
        for i in range(1, len(closes)):
            tr = max(
                highs[i] - lows[i],
                abs(highs[i] - closes[i-1]),
                abs(lows[i] - closes[i-1])
            )
            true_ranges.append(tr)
        return float(np.mean(true_ranges[-self.atr_period:]))
    
    def _calculate_atr_from_closes(self, closes: List[float]) -> float:
        """Calcula ATR simplificado a partir de closes."""
        if len(closes) < 15:
            return closes[-1] * 0.02 if closes else 0.02
        
        returns = np.diff(closes[-15:]) / closes[-16:-1]
        return float(np.mean(np.abs(returns)) * closes[-1])


setup_recommendation_engine = SetupRecommendationEngine()
