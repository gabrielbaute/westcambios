"""
Base methods and class for controllers
"""
import logging
from typing import Any
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from app.database.db_config import SessionLocal

class BaseController:
    """
    Base controller for handling database operations with explicit session management.
    """
    def __init__(self) -> None:
        """
        Initializes the controller with a dedicated database session and logger.
        """
        self.logger = logging.getLogger(self.__class__.__name__)
        self.session: Session = SessionLocal()

    def _commit_or_rollback(self, record: Any) -> bool:
        """
        Internal helper to commit a new record or rollback on error.

        Args:
            record (object): The SQLAlchemy model instance to be saved.

        Returns:
            bool: True if the operation was successful, False otherwise.
        """
        try:
            self.session.add(record)
            self.session.commit()
            self.logger.info(f"Successfully committed: {record}")
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            self.logger.error(f"SQLAlchemy Error during commit: {e}")
            return False

    def _update_or_rollback(self, record: Any) -> bool:
        """
        Internal helper to update an existing record or rollback on error.

        Args:
            record (object): The SQLAlchemy model instance to be updated.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        try:
            self.session.add(record)
            self.session.commit()
            self.logger.info(f"Successfully updated: {record}")
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            self.logger.error(f"SQLAlchemy Error during update: {e}")
            return False

    def _delete_or_rollback(self, record: Any) -> bool:
        """
        Internal helper to delete a record or rollback on error.

        Args:
            record (object): The SQLAlchemy model instance to be deleted.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        try:
            self.session.delete(record)
            self.session.commit()
            self.logger.info(f"Successfully deleted: {record}")
            return True
        except SQLAlchemyError as e:
            self.session.rollback()
            self.logger.error(f"SQLAlchemy Error during deletion: {e}")
            return False

    def close_session(self) -> None:
        """
        Manually closes the database session. 
        Should be called when the controller is no longer needed.
        """
        self.session.close()
        self.logger.debug("Database session closed.")