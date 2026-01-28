import logging
from pytz import timezone
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler

from app.enums import CurrencyEnum
from app.controllers import RateController
from app.services.binance_service import BinanceP2P
from app.schemas import RateCreate, RateResponse, BinanceResponse

class SchedulerService:
    """
    Service for scheduling background tasks.
    """
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.binance = BinanceP2P()
        self.rate_controller = RateController()
        self.scheduler = BackgroundScheduler(timezone=timezone('America/Caracas'))
    
    def save_binance_rate(self) -> bool:
        """
        Save Binance rates to database

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            pair = self.binance.get_usdt_ves_pair()
            self.logger.info(f"Saving Binance rate: {pair.average_price} {pair.fiat}/{pair.asset}")
            rate = RateCreate(
                from_currency=CurrencyEnum.VES,
                to_currency=CurrencyEnum.USDT,
                rate=pair.average_price,
                timestamp=datetime.now()   
            )
            self.rate_controller.register_rate(rate)
            return True
        except Exception as e:
            self.logger.error(f"Error saving Binance rate: {e}")
            return False
    
    def scheduler_jobs(self):
        """
        Scheduler jobs.
        """
        self.scheduler.add_job(
            func=self.save_binance_rate, 
            trigger="cron",
            hour="0,6,12,18",
            minute="0",
            second="0",
            id="save_binance_rate", 
            name="Save Binance rate", 
            )
    
    def start_scheduler(self):
        """
        Start the scheduler.
        """
        self.logger.info("Starting scheduler...")
        self.scheduler_jobs()
        self.scheduler.start()
    
    def stop_scheduler(self):
        """
        Stop the scheduler.
        """
        self.scheduler.shutdown()