"""
User controller
"""
import logging
from datetime import date
from typing import Optional

from app.schemas import UserCreate, UserResponse, UserUpdate, UserListResponse
from app.controllers.base_controller import BaseController
from app.database.models import UsersDatabaseModel
from app.enums import UserRole

class UserController(BaseController):
    """
    Controller for managing users in the database.
    """
    def __init__(self) -> None:
        """
        Initializes the controller with a dedicated database session and logger.
        """
        super().__init__()
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def register_user(self, user: UserCreate) -> Optional[UserResponse]:
        """
        Creates a new user record in the database.

        Args:
            user(UserCreate): User data to be created.

        Returns:
            Optional[UserResponse]: User record created.
        """
        try:
            new_user = UsersDatabaseModel(**user.model_dump())
            if not self._commit_or_rollback(new_user):
                return None
            self.logger.info(f"Successfully created new user record: {new_user}")
            self.session.refresh(new_user)
            return UserResponse.model_validate(new_user)
        except Exception as e:
            self.logger.error(f"Error creating new user record: {e}")
            return None
    
    def get_user_by_id(self, user_id: int) -> Optional[UserResponse]:
        """
        Retrieves a user record by its ID from the database.

        Args:
            user_id(int): ID of the user record to be retrieved.

        Returns:
            Optional[UserResponse]: User record retrieved.
        """
        try:
            user = self._get_item_by_id(UsersDatabaseModel, user_id)
            if user:
                self.logger.info(f"Successfully retrieved user record: {user}")
                return UserResponse.model_validate(user)
            else:
                self.logger.warning(f"User record with ID {user_id} not found.")
                return None
        except Exception as e:
            self.logger.error(f"Error retrieving user record: {e}")
            return None
    
    def get_user_by_email(self, email: str) -> Optional[UserResponse]:
        """
        Retrieves a user record by its email from the database.

        Args:
            email(str): Email
        
        Returns:
            Optional[UserResponse]: User record retrieved.
        """
        try:
            user = self.session.query(UsersDatabaseModel).filter(UsersDatabaseModel.email == email).one_or_none()
            if user:
                self.logger.info(f"Successfully retrieved user record by email: {user}")
                return UserResponse.model_validate(user)
            else:
                self.logger.warning(f"User record with email {email} not found.")
                return None
        except Exception as e:
            self.logger.error(f"Error retrieving user record by email: {e}")
            return None

    def get_user_by_role(self, user_role: UserRole) -> UserListResponse:
        """
        Retrieves a list of users with a specific role from the database.

        Args:
            user_role(UserRole): Role of the users to be retrieved.

        Returns:
            UserListResponse: List of users with the specified role.
        """
        try:
            users_response = self.session.query(UsersDatabaseModel).filter(UsersDatabaseModel.role == user_role).all()
            if users_response:
                list_response = UserListResponse(
                    count=len(users_response), 
                    users=[UserResponse.model_validate(user) for user in users_response]
                    )
                self.logger.info(f"Successfully retrieved users with role {user_role}: {list_response.count} users found.")
                return list_response
        except Exception as e:
            self.logger.error(f"Error retrieving users with role {user_role}: {e}")
            return UserListResponse(count=0, users=[])

    def get_users_register_by_time_range(self, start_date: date, end_date: date) -> UserListResponse:
        """
        Retrieves a list of users registered within a specified time range from the database.

        Args:
            start_date(date): Start date of the time range.
            end_date(date): End date of the time range.

        Returns:
            UserListResponse: List of users registered within the specified time range.
        """
        try:
            users = self.session.query(UsersDatabaseModel).filter(
                UsersDatabaseModel.created_at >= start_date,
                UsersDatabaseModel.created_at <= end_date
            ).all()
            if users:
                list_response = UserListResponse(
                    count=len(users), 
                    users=[UserResponse.model_validate(user) for user in users]
                    )
                self.logger.info(f"Successfully retrieved users within time range: {list_response.count} users found.")
                return list_response
        except Exception as e:
            self.logger.error(f"Error retrieving users within time range: {e}")
            return UserListResponse(count=0, users=[])

    def get_all_users(self) -> UserListResponse:
        """
        Retrieves a list of all users from the database.

        Returns:
            UserListResponse: List of all users.
        """
        try:
            users = self.session.query(UsersDatabaseModel).all()
            if users:
                list_response = UserListResponse(
                    count=len(users),
                    users=[UserResponse.model_validate(user) for user in users]
                )
                self.logger.info(f"Successfully retrieved all users: {list_response.count} users found.")
                return list_response
        except Exception as e:
            self.logger.error(f"Error retrieving all users: {e}")
            return UserListResponse(count=0, users=[])
    
    def update_user(self, user_id: int, user: UserUpdate) -> Optional[UserResponse]:
        """
        Updates an existing user record in the database.

        Args:
            user_id(int): ID of the user record to be updated.
            user(UserUpdate): Updated user data.

        Returns:
            Optional[UserResponse]: Updated user record.
        """
        try:
            user_record = self._get_item_by_id(UsersDatabaseModel, user_id)
            if user_record:
                for key, value in user.model_dump(exclude_unset=True).items():
                    setattr(user_record, key, value)
                self._update_or_rollback(user_record)
                self.logger.info(f"Successfully updated user record: {user_record}")
                self.session.refresh(user_record)
                return UserResponse.model_validate(user_record)
        except Exception as e:
            self.logger.error(f"Error updating user record: {e}")
            return None
    
    def delete_user(self, user_id: int) -> bool:
        """
        Deletes a user record from the database.

        Args:
            user_id(int): ID of the user record to be deleted.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        try:
            user = self._get_item_by_id(UsersDatabaseModel, user_id)
            if user:
                self._delete_or_rollback(user)
                self.logger.info(f"Successfully deleted user record: {user}")
                return True
        except Exception as e:
            self.logger.error(f"Error deleting user record: {e}")
            return False