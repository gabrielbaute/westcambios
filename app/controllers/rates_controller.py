"""
Rates exchange controller
"""
import logging
from datetime import date
from typing import Optional

from app.schemas import RateCreate, RateResponse, RateUpdate, RateListResponse
from app.controllers.base_controller import BaseController
from app.database.models import RatesDatabaseModel

class RateController(BaseController):
    """
    Controller for managing rates in the database.
    """
    def __init__(self) -> None:
        """
        Initializes the controller with a dedicated database session and logger.
        """
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def register_rate(self, rate: RateCreate) -> Optional[RateResponse]:
        """
        Creates a new rate record in the database.
        
        Args:
            rate(RateCreate): Rate data to be created.
        
        Returns:
            Optional[RateResponse]: Rate record created.
        """
        try:
            new_rate = RatesDatabaseModel(**rate.model_dump())
            self._commit_or_rollback(new_rate)
            self.logger.info(f"Successfully created new rate record: {new_rate}")
            self.session.refresh(new_rate)
            return RateResponse.model_validate(new_rate)
        except Exception as e:
            self.logger.error(f"Error creating new rate record: {e}")
            return None
    
    def get_rate_by_id(self, rate_id: int) -> Optional[RateResponse]:
        """
        Retrieves a rate record by its ID from the database.

        Args:
            rate_id(int): ID of the rate record to be retrieved.

        Returns:
            Optional[RateResponse]: Rate record retrieved.
        """
        try:
            rate = self.session.query(RatesDatabaseModel).filter(RatesDatabaseModel.id == rate_id).first()
            if rate:
                self.logger.info(f"Successfully retrieved rate record: {rate}")
                return RateResponse.model_validate(rate)
            else:
                self.logger.warning(f"Rate record with ID {rate_id} not found.")
                return None
        except Exception as e:
            self.logger.error(f"Error retrieving rate record: {e}")
            return None

    def get_rates_by_time_range(self, start_date: date, end_date: date) -> RateListResponse:
        """
        Retrieves a list of rates within a specified time range from the database.

        Args:
            start_date(date): Start date of the time range.
            end_date(date): End date of the time range.

        Returns:
            RateListResponse: List of rates within the specified time range.
        """
        try:
            rates = self.session.query(RatesDatabaseModel).filter(
                RatesDatabaseModel.timestamp >= start_date,
                RatesDatabaseModel.timestamp <= end_date
            ).all()
            if rates:
                list_response = RateListResponse(
                    count=len(rates), 
                    rates=[RateResponse.model_validate(rate) for rate in rates]
                    )
                self.logger.info(f"Successfully retrieved rates within time range: {list_response.count} records found.")
                return list_response
        except Exception as e:
            self.logger.error(f"Error retrieving rates within time range: {e}")
            return RateListResponse(count=0, rates=[])


    def update_rate_record(self, rate_id: int, rate: RateUpdate) -> Optional[RateResponse]:
        """
        Updates an existing rate record in the database.
        
        Args:
            rate_id(int): ID of the rate record to be updated.
            rate(RateUpdate): Updated rate data.
        
        Returns:
            Optional[RateResponse]: Updated rate record.
        """
        try:
            rate_record = self.session.query(RatesDatabaseModel).filter(RatesDatabaseModel.id == rate_id).first()
            if rate_record:
                for key, value in rate.model_dump(exclude_unset=True).items():
                    setattr(rate_record, key, value)
                self._update_or_rollback(rate_record)
                self.logger.info(f"Successfully updated rate record: {rate_record}")
                self.session.refresh(rate_record)
                return RateResponse.model_validate(rate_record)
        except Exception as e:
            self.logger.error(f"Error updating rate record: {e}")
            return None
    
    def delete_rate_record(self, rate_id: int) -> bool:
        """
        Deletes a rate record from the database.

        Args:
            rate_id(int): ID of the rate record to be deleted.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        try:
            rate_record = self.session.query(RatesDatabaseModel).filter(RatesDatabaseModel.id == rate_id).first()
            if rate_record:
                self._delete_or_rollback(rate_record)
                self.logger.info(f"Successfully deleted rate record: {rate_record}")
                return True
        except Exception as e:
            self.logger.error(f"Error deleting rate record: {e}")
            return False
