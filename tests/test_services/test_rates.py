import pytest
from datetime import datetime
from app.services.rates_service import RateService
from app.schemas import RateCreate, RateListResponse
from app.enums import CurrencyEnum

class TestRateService:
    def setup_method(self):
        self.service = RateService()

    def teardown_method(self):
        self.service.controller.close_session()

    def test_register_and_get_today_rates(self):
        """
        Test that registering a rate and retrieving today's rates works.
        """
        # 1. Crear una tasa para hoy
        new_rate = RateCreate(
            from_currency=CurrencyEnum.BRL,
            to_currency=CurrencyEnum.VES,
            rate=100.0,
            timestamp=datetime.now()
        )
        
        registered = self.service.register_rate(new_rate)
        assert registered is not None
        assert registered.rate == 100.0

        # 2. Recuperar tasas de hoy
        response = self.service.get_today_rates()
        
        assert isinstance(response, RateListResponse)
        assert len(response.rates) >= 1
        # Verificar que al menos una tasa coincida con la que creamos
        assert any(r.rate == 100.0 for r in response.rates)

    def test_get_range_logic(self):
        """
        Verify that the range logic returns a RateListResponse even if empty.
        """
        # Probamos un rango de 7 días (week)
        response = self.service.get_last_week_rates()
        assert isinstance(response, RateListResponse)
        assert isinstance(response.rates, list)