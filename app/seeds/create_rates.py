"""
Seed for test rates logic
"""
from datetime import datetime, timedelta
from app.schemas import RateCreate
from app.services import RateService
from app.enums import CurrencyEnum

def create_rates():
    rate_service = RateService()
    rate_in = RateCreate(
        from_currency=CurrencyEnum.BRL,
        to_currency=CurrencyEnum.VES,
        rate=95.5,
        timestamp=datetime.now()
    )
    yesterday_rate = RateCreate(
        from_currency=CurrencyEnum.BRL,
        to_currency=CurrencyEnum.VES,
        rate=94.2,
        timestamp=datetime.now() - timedelta(days=1)
    )
    two_days_ago_rate = RateCreate(
        from_currency=CurrencyEnum.BRL,
        to_currency=CurrencyEnum.VES,
        rate=93.8,
        timestamp=datetime.now() - timedelta(days=2)
    )
    rates = [rate_in, yesterday_rate, two_days_ago_rate]
    for rate in rates:
        rate_service.register_rate(rate)
    rate_service.dispose()

if __name__ == "__main__":
    create_rates()