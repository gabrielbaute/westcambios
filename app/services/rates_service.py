"""
Module for rates service and business logic
"""
import logging
from datetime import date, datetime, timedelta
from typing import Optional

from app.controllers import RateController
from app.schemas import RateCreate, RateResponse, RateUpdate, RateListResponse

class RateService:
    """
    Service for managing rates.
    """
    def __init__(self):
        self.controller = RateController()
        self.logger = logging.getLogger(self.__class__.__name__)

    def _get_range_response(self, days: int) -> RateListResponse:
            """
            Helper to calculate date ranges and fetch records.
            """
            today = datetime.now().date()
            start_date = today - timedelta(days=days)
            self.logger.debug(f"Retrieving rates from {start_date} to {today}")
            return self.controller.get_rates_by_time_range(start_date, today)

    def register_rate(self, rate_data: RateCreate) -> Optional[RateResponse]:
        """
        Register a new rate.

        Args:
            rate_data (RateCreate): The rate data to be registered.

        Returns:
            RateResponse: The registered rate record.
        """
        if not rate_data.timestamp:
            rate_data.timestamp = datetime.now()
        self.logger.debug(f"Creating rate: {rate_data}")
        return self.controller.register_rate(rate_data)
    
    def get_rate_by_id(self, rate_id: int) -> Optional[RateResponse]:
        """
        Get a rate by its ID.

        Args:
            rate_id (int): The ID of the rate to retrieve.

        Returns:
            RateResponse: The retrieved rate record.
        """
        self.logger.debug(f"Retrieving rate with ID: {rate_id}")
        return self.controller.get_rate_by_id(rate_id)
    
    def get_all_rates(self) -> RateListResponse:
        """
        Get all rates.

        Returns:
            RateListResponse: List of all rate records.
        """
        self.logger.debug("Retrieving all rates")
        return self.controller.get_all_rates()
    
    def get_today_rates(self) -> RateListResponse:
        """
        Get rates for today.

        Returns:
            RateListResponse: List of today's rate records.
        """
        return self._get_range_response(days=0)
    
    def get_last_week_rates(self) -> RateListResponse:
        """
        Get rates for the last week.

        Returns:
            RateListResponse: List of last week's rate records.
        """
        return self._get_range_response(days=7)
    
    def get_last_month_rates(self) -> RateListResponse:
        """
        Get rates for the last month.

        Returns:
            RateListResponse: List of last month's rate records.
        """
        return self._get_range_response(days=30)
    
    def get_last_3_months_rates(self) -> RateListResponse:
        """
        Get rates for the last 3 months.

        Returns:
            RateListResponse: List of last 3 months' rate records.
        """
        return self._get_range_response(days=90)
    
    def get_last_6_months_rates(self) -> RateListResponse:
        """
        Get rates for the last 6 months.

        Returns:
            RateListResponse: List of last 6 months' rate records.
        """
        return self._get_range_response(days=180)
    
    def get_last_year_rates(self) -> RateListResponse:
        """
        Get rates for the last year.

        Returns:
            RateListResponse: List of last year's rate records.
        """
        return self._get_range_response(days=365)
    
    def get_rates_by_custom_range(self, start_date: date, end_date: date) -> RateListResponse:
        """
        Get rates within a specified date range.

        Args:
            start_date (date): The start date of the date range.
            end_date (date): The end date of the date range.

        Returns:
            RateListResponse: List of rate records within the specified date range.
        """
        return self.controller.get_rates_by_time_range(start_date, end_date)
    
    def update_rate(self, rate_id: int, rate_data: RateUpdate) -> Optional[RateResponse]:
        """
        Update an existing rate.

        Args:
            rate_id (int): The ID of the rate to update.
            rate_data (RateUpdate): The updated rate data.

        Returns:
            RateResponse: The updated rate record.
        """
        self.logger.debug(f"Updating rate with ID: {rate_id} with data: {rate_data}")
        return self.controller.update_rate_record(rate_id, rate_data)
    
    def delete_rate(self, rate_id: int) -> bool:
        """
        Delete a rate by its ID.

        Args:
            rate_id (int): The ID of the rate to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        self.logger.debug(f"Deleting rate with ID: {rate_id}")
        return self.controller.delete_rate_record(rate_id)

    def dispose(self) -> None:
            """
            Closes the underlying controller session.
            """
            self.controller.close_session()