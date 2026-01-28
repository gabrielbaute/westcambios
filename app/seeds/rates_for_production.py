"""
Seed for test rates logic
"""
from datetime import datetime, timedelta
from app.schemas import RateCreate
from app.services import RateService
from app.enums import CurrencyEnum

def create_rates_production():
    rate_service = RateService()
    
    # Verifying rates register already exists
    if rate_service.get_all_rates():
            return
    
    rates = [
            RateCreate(
                from_currency=CurrencyEnum.USDT,
                to_currency=CurrencyEnum.BRL,
                rate=5.46,
                timestamp=datetime.now()
            ),
            RateCreate(
                from_currency=CurrencyEnum.USD,
                to_currency=CurrencyEnum.VES,
                rate=361.49,
                timestamp=datetime.now()
            ),
            RateCreate(
                from_currency=CurrencyEnum.BRL,
                to_currency=CurrencyEnum.VES,
                rate=92.0,
                timestamp=datetime.now()
            ),
            RateCreate(
                from_currency=CurrencyEnum.BRL,
                to_currency=CurrencyEnum.VES,
                rate=91.0,
                timestamp=datetime.now() - timedelta(days=1)
            ),
            RateCreate(
                from_currency=CurrencyEnum.BRL,
                to_currency=CurrencyEnum.VES,
                rate=82.0,
                timestamp=datetime.now() - timedelta(days=2)
            ),
            RateCreate(
                from_currency=CurrencyEnum.BRL,
                to_currency=CurrencyEnum.VES,
                rate=82.0,
                timestamp=datetime.now() - timedelta(days=3)
            ),
            RateCreate(
                from_currency=CurrencyEnum.BRL,
                to_currency=CurrencyEnum.VES,
                rate=82.0,
                timestamp=datetime.now() - timedelta(days=4)
            ),
            RateCreate(
                from_currency=CurrencyEnum.BRL,
                to_currency=CurrencyEnum.VES,
                rate=80.0,
                timestamp=datetime.now() - timedelta(days=5)
            ),
            RateCreate(
                from_currency=CurrencyEnum.BRL,
                to_currency=CurrencyEnum.VES,
                rate=80.0,
                timestamp=datetime.now() - timedelta(days=6)
            ),
            RateCreate(
                from_currency=CurrencyEnum.BRL,
                to_currency=CurrencyEnum.VES,
                rate=78.50,
                timestamp=datetime.now() - timedelta(days=7)
            ),
            RateCreate(
                from_currency=CurrencyEnum.BRL,
                to_currency=CurrencyEnum.VES,
                rate=76.0,
                timestamp=datetime.now() - timedelta(days=8)
            ),
        ]   
    for rate in rates:
        rate_service.register_rate(rate)
    rate_service.dispose()