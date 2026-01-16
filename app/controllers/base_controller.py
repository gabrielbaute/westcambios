"""
Base methods and class for controllers
"""
import logging
from typing import Any, Optional, Type
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

    def _get_item_by_id(self, model: Type[Any], item_id: int) -> Optional[Any]:
        """
        Retrieves an item by its ID from the database using the Identity Map.

        Args:
            model (Type[Any]): The SQLAlchemy model class to query.
            item_id (int): The primary key ID of the item.

        Returns:
            Optional[Any]: The retrieved model instance or None if not found/error.
        """
        try:
            # session.get es la forma preferida para búsquedas por PK en SQLAlchemy 2.0
            item = self.session.get(model, item_id)
            if item:
                self.logger.info(f"Successfully retrieved {model.__tablename__} ID: {item_id}")
                return item
            
            self.logger.warning(f"{model.__tablename__} with ID {item_id} not found.")
            return None
        except SQLAlchemyError as e:
            self.logger.error(f"SQLAlchemy Error during retrieval of {model.__tablename__}: {e}")
            return None
    
    def close_session(self) -> None:
        """
        Manually closes the database session. 
        Should be called when the controller is no longer needed.
        """
        self.session.close()
        self.logger.debug("Database session closed.")