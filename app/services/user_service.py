"""
Module for users service and business logic
"""
import logging
from typing import Optional
from datetime import date, datetime, timedelta

from app.schemas import UserCreate, UserResponse, UserUpdate, UserListResponse
from app.services.security_service import SecurityService
from app.controllers import UserController
from app.enums import UserRole

class UserService:
    """
    Service for managing users.
    """
    def __init__(self):
        self.controller = UserController()
        self.logger = logging.getLogger(self.__class__.__name__)

    def _get_range_response(self, days: int) -> UserListResponse:
        """
        Helper to calculate date ranges and fetch records.

        Args:
            days (int): Number of days to subtract from today.

        Returns:
            UserListResponse: List of user records within the specified date range.           
        """
        today = datetime.now().date()
        start_date = today - timedelta(days=days)
        self.logger.debug(f"Retrieving users from {start_date} to {today}")
        return self.controller.get_users_register_by_time_range(start_date, today)

    def _validate_email_exists(self, email: str) -> bool:
        """
        Validate if an email already exists in the database.

        Args:
            email (str): The email to validate.

        Returns:
            bool: True if the email already exists, False otherwise.
        """
        try:
            user = self.controller.get_user_by_email(email)
            if user:
                self.logger.warning(f"User with email {email} already exists.")
                return True
            else:
                return False
        except Exception as e:
            self.logger.error(f"Error validating email: {e}")
            return False

    def register_user(self, user_data: UserCreate) -> Optional[UserResponse]:
        """
        Register a new user.

        Args:
            user_data (UserCreate): The user data to be registered.

        Returns:
            UserResponse: The registered user record.
        """
        self.logger.debug(f"Creating user: {user_data}")
        if self._validate_email_exists(user_data.email):
            return None
        user_data.password_hash = SecurityService.get_password_hash(user_data.password_hash)
        user_data.created_at = datetime.now()
        return self.controller.register_user(user_data)
    
    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """
        Get a user by its ID.

        Args:
            user_id (int): The ID of the user to retrieve.

        Returns:
            UserResponse: The retrieved user record.
        """
        self.logger.debug(f"Retrieving user with ID: {user_id}")
        return self.controller.get_user_by_id(user_id)

    def get_users_by_role(self, user_role: UserRole) -> Optional[UserListResponse]:
        """
        Get users by role

        Args:
            user_role (UserRole): The role of the users to retrieve.

        Returns:
            UserListResponse: List of user records with the specified role.
        """
        self.logger.debug(f"Retrieving users with role: {user_role}")
        return self.controller.get_user_by_role(user_role)    

    def get_all_users(self) -> Optional[UserListResponse]:
        """
        Get all users.

        Returns:
            UserListResponse: List of all user records.
        """
        self.logger.debug("Retrieving all users")
        return self.controller.get_all_users()
    
    def get_user_register_last_month(self) -> UserListResponse:
        """
        Get users registered in the last month.

        Returns:
            UserListResponse: List of last month's user records.
        """
        return self._get_range_response(days=30)
    
    def get_user_register_last_3_months(self) -> UserListResponse:
        """
        Get users registered in the last 3 months.

        Returns:
            UserListResponse: List of last 3 months' user records.
        """
        return self._get_range_response(days=90)
    
    def get_user_register_last_6_months(self) -> UserListResponse:
        """
        Get users registered in the last 6 months.

        Returns:
            UserListResponse: List of last 6 months' user records.
        """
        return self._get_range_response(days=180)
    
    def get_user_register_last_year(self) -> UserListResponse:
        """
        Get users registered in the last year.

        Returns:
            UserListResponse: List of last year's user records.
        """
        return self._get_range_response(days=365)
    
    def get_users_by_custom_range(self, start_date: date, end_date: date) -> UserListResponse:
        """
        Get users registered within a specified date range.
        
        Args:
            start_date (date): The start date of the date range.
            end_date (date): The end date of the date range.

        Returns:
            UserListResponse: List of user records within the specified date range.
        """
        return self.controller.get_users_register_by_time_range(start_date, end_date)


    
    def update_user_data(self, user_id: int, user_data: UserUpdate) -> Optional[UserResponse]:
        """
        Update user data

        Args:
            user_id (int): The ID of the user to update.
            user_data (UserUpdate): The updated user data.

        Returns:
            UserResponse: The updated user record.
        """
        self.logger.debug(f"Updating user with ID: {user_id} with data: {user_data}")
        user_data.updated_at = datetime.now()
        return self.controller.update_user(user_id, user_data)
    
    def update_user_password_hash(self, user_id: int, password_hash: str) -> Optional[UserResponse]:
        """
        Update user password hash

        Args:
            user_id (int): The ID of the user to update.
            password_hash (str): The updated password hash.

        Returns:
            UserResponse: The updated user record.
        """
        self.logger.debug(f"Updating user password hash with ID: {user_id}")
        user_data = UserUpdate(
            password_hash=password_hash,
            updated_at=datetime.now()
            )
        return self.controller.update_user(user_id, user_data)
    
    def update_user_role(self, user_id: int, user_role: UserRole) -> Optional[UserResponse]:
        """
        Update user role

        Args:
            user_id (int): The ID of the user to update.
            user_role (UserRole): The updated user role.

        Returns:
            UserResponse: The updated user record.
        """
        self.logger.debug(f"Updating user role with ID: {user_id}")
        user_data = UserUpdate(
            role=user_role,
            updated_at=datetime.now()
            )
        return self.controller.update_user(user_id, user_data)

    def update_user_email(self, user_id: int, email: str) -> Optional[UserResponse]:
        """
        Update user email

        Args:
            user_id (int): The ID of the user to update.
            email (str): The updated email.

        Returns:
            UserResponse: The updated user record.
        """
        self.logger.debug(f"Updating user email with ID: {user_id}")
        user_data = UserUpdate(
            email=email,
            updated_at=datetime.now()
            )
        return self.controller.update_user(user_id, user_data)

    def activate_user(self, user_id: int) -> Optional[UserResponse]:
        """
        Activate a user

        Args:
            user_id (int): The ID of the user to activate.

        Returns:
            UserResponse: The activated user record.
        """
        self.logger.debug(f"Activating user with ID: {user_id}")
        user_data = UserUpdate(
            is_active=True,
            updated_at=datetime.now()
            )
        return self.controller.update_user(user_id, user_data)
    
    def deactivate_user(self, user_id: int) -> Optional[UserResponse]:
        """
        Deactivate a user

        Args:
            user_id (int): The ID of the user to deactivate.

        Returns:
            UserResponse: The deactivated user record.
        """
        self.logger.debug(f"Deactivating user with ID: {user_id}")
        user_data = UserUpdate(
            is_active=False,
            updated_at=datetime.now()
            )
        return self.controller.update_user(user_id, user_data)

    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user

        Args:
            user_id (int): The ID of the user to delete.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        self.logger.debug(f"Deleting user with ID: {user_id}")
        return self.controller.delete_user(user_id)
    
    def dispose(self) -> None:
        """
        Closes the underlying controller session.
        """
        self.controller.close_session()
        self.logger.debug("Controller session closed.")