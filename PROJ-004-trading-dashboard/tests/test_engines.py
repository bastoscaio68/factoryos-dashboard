import pytest
from datetime import datetime, timezone
from src.services.regime_detection import RegimeDetectionEngine
from src.services.setup_recommendation import SetupRecommendationEngine


class TestRegimeDetection:
    """Testes para engine de detecção de regime."""
    
    @pytest.fixture
    def engine(self):
        return RegimeDetectionEngine()
    
    def test_detect_bull_trend(self, engine):
        """Testa detecção de tendência de alta."""
        # Dados de preço em tendência de alta
        closes = [100 + i * 0.5 for i in range(60)]
        highs = [c * 1.02 for c in closes]
        lows = [c * 0.98 for c in closes]
        
        result = engine.detect_regime("BTC", highs, lows, closes)
        
        assert result["symbol"] == "BTC"
        assert "bull_trend" in result["regime_type"]
        assert 0 <= result["confidence"] <= 1
        assert "features" in result
    
    def test_detect_sideways(self, engine):
        """Testa detecção de mercado lateral."""
        # Dados de preço lateral
        import numpy as np
        closes = [100 + np.sin(i/5) * 2 for i in range(60)]
        highs = [c * 1.01 for c in closes]
        lows = [c * 0.99 for c in closes]
        
        result = engine.detect_regime("ETH", highs, lows, closes)
        
        assert result["symbol"] == "ETH"
        assert "confidence" in result
    
    def test_insufficient_data(self, engine):
        """Testa resposta com dados insuficientes."""
        closes = [100, 101, 102]
        highs = [102, 103, 104]
        lows = [98, 99, 100]
        
        result = engine.detect_regime("SOL", highs, lows, closes)
        
        assert result["regime_type"] == "sideways"
        assert "insufficient" in result["features"]["error"].lower()


class TestSetupRecommendation:
    """Testes para engine de recomendação de setup."""
    
    @pytest.fixture
    def engine(self):
        return SetupRecommendationEngine()
    
    def test_breakout_detection(self, engine):
        """Testa detecção de breakout."""
        # Criar dados com breakout
        closes = [100] * 20 + [105, 106, 107]
        highs = [c * 1.02 for c in closes]
        lows = [c * 0.98 for c in closes]
        volume = [1000] * 20 + [5000, 6000, 7000]
        
        candidates = engine.get_all_candidates("BTC", closes, highs, lows, volume)
        
        # Deve encontrar pelo menos um candidato de breakout
        breakout_candidates = [c for c in candidates if "Breakout" in c.name]
        assert len(breakout_candidates) > 0
    
    def test_ma_crossover(self, engine):
        """Testa detecção de cruzamento de médias móveis."""
        import numpy as np
        # Criar golden cross
        t = np.linspace(0, 50, 100)
        slow = 100 + t * 0.5
        fast = 95 + t * 0.6  # Cruza de baixo para cima
        
        closes = list(slow) + list(fast[-10:])  # Simular dados
        
        candidate = engine.detect_moving_average_crossover("BTC", closes, fast=9, slow=21)
        
        assert candidate is not None
        assert candidate.direction == "long"
    
    def test_candidates_sorted_by_confidence(self, engine):
        """Testa ordenação de candidatos por confiança."""
        closes = [100] * 20 + [105, 106, 107]
        highs = [c * 1.02 for c in closes]
        lows = [c * 0.98 for c in closes]
        volume = [1000] * 20 + [5000, 6000, 7000]
        
        candidates = engine.get_all_candidates("BTC", closes, highs, lows, volume)
        
        # Verificar ordenação
        if len(candidates) > 1:
            for i in range(len(candidates) - 1):
                assert candidates[i].confidence >= candidates[i + 1].confidence


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
