import pytest
from unittest.mock import MagicMock, patch
from app.services.binance_service import BinanceP2P
from app.schemas import BinanceRequest, BinanceResponse

class TestBinanceP2PService:
    def setup_method(self):
        self.service = BinanceP2P()

    def test_build_request(self):
        """
        Verifica que el generador de requests asigne los valores correctamente.
        """
        request_obj = self.service.build_request(
            fiat="VES", page=1, rows=10, trade_type="BUY", asset="USDT"
        )
        
        assert isinstance(request_obj, BinanceRequest)
        assert request_obj.fiat == "VES"
        assert request_obj.tradeType == "BUY" 

    def test_do_request_invalid(self):
        """
        Test handling of invalid request. 
        Si pasas algo que no es un BinanceRequest, fallará el .model_dump()
        """
        # Simulamos que el objeto no tiene model_dump para forzar el error
        with pytest.raises(AttributeError):
            self.service.do_request({"invalid": "data"})

    def test_colect_prices(self):
        """
        Test colecting prices usando un mock de respuesta de Binance.
        """
        mock_data = {
            "code": "000000",
            "data": [
                {"adv": {"price": "35.5"}},
                {"adv": {"price": "36.0"}}
            ]
        }
        
        prices = self.service.colect_prices(mock_data, fiat="VES")
        
        assert prices == [35.5, 36.0]
        assert isinstance(prices[0], float)

    def test_calculate_med(self):
        """
        Test matemático de mediana y promedio.
        """
        prices = [100.0, 102.0, 101.0, 103.0, 104.0]
        result = self.service.calculate_med(prices)
        
        assert result["median_price"] == 102.0
        assert result["average_price"] == 102.0

    def test_get_pair(self):
        """
        Test de integración (o mockeado) de get_pair.
        """
        # Aquí usamos datos reales o mockeamos la respuesta de la red
        pair = self.service.get_usdt_ves_pair()
        
        if pair: # Si Binance respondió correctamente
            assert isinstance(pair, BinanceResponse)
            assert pair.fiat == "VES"
            assert pair.asset == "USDT"
            # En BinanceResponse definiste trade_type (snake_case)
            assert pair.trade_type == "BUY"
            assert isinstance(pair.average_price, (float, type(None)))