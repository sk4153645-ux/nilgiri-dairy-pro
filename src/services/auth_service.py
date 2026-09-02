"""
Authentication Service

Handles user authentication and session management.
"""

import bcrypt
from typing import Tuple, Optional
from src.database.connection import get_db
from src.core.exceptions import AuthenticationError, ValidationError
from src.core.validators import validate_email
from src.logger import setup_logger

logger = setup_logger(__name__)


class AuthService:
    """
    Authentication and authorization service.

    Features:
        - User registration
        - Login with password hashing
        - Session management
        - Password validation
    """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hash password using bcrypt.

        Args:
            password: Plain text password

        Returns:
            Hashed password
        """
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """
        Verify password against hash.

        Args:
            password: Plain text password
            password_hash: Hashed password

        Returns:
            True if password matches
        """
        return bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8'))

    @staticmethod
    def register(email: str, password: str, dairy_name: str, dairy_phone: str = "") -> Tuple[bool, str]:
        """
        Register new user.

        Args:
            email: User email
            password: User password
            dairy_name: Name of dairy
            dairy_phone: Dairy phone number

        Returns:
            Tuple of (success, message)
        """
        try:
            # Validate email
            _, email = validate_email(email)

            # Validate password
            if len(password) < 6:
                raise ValidationError("Password must be at least 6 characters", field="password")

            # Check if user already exists
            db = get_db()
            existing = db.execute_query(
                "SELECT id FROM users WHERE email = ?",
                (email,),
                fetch_one=True,
            )
            if existing:
                raise ValidationError("Email already registered", field="email")

            # Hash password
            password_hash = AuthService.hash_password(password)

            # Create user
            db.execute_insert(
                """
                INSERT INTO users (email, password_hash, dairy_name, dairy_phone)
                VALUES (?, ?, ?, ?)
                """,
                (email, password_hash, dairy_name, dairy_phone),
            )

            logger.info(f"User registered: {email}")
            return True, "Registration successful"
        except ValidationError as e:
            logger.warning(f"Registration failed: {e}")
            return False, str(e)
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return False, "Registration failed. Please try again."

    @staticmethod
    def login(email: str, password: str) -> Tuple[bool, str, Optional[dict]]:
        """
        Authenticate user.

        Args:
            email: User email
            password: User password

        Returns:
            Tuple of (success, message, user_data)
        """
        try:
            # Validate email format
            _, email = validate_email(email)

            # Get user from database
            db = get_db()
            user = db.execute_query(
                "SELECT * FROM users WHERE email = ? AND is_active = 1",
                (email,),
                fetch_one=True,
            )

            if not user:
                logger.warning(f"Login attempt failed: user not found - {email}")
                raise AuthenticationError("Invalid email or password")

            # Verify password
            if not AuthService.verify_password(password, user['password_hash']):
                logger.warning(f"Login attempt failed: wrong password - {email}")
                raise AuthenticationError("Invalid email or password")

            logger.info(f"User logged in: {email}")
            return True, "Login successful", dict(user)
        except AuthenticationError as e:
            return False, str(e), None
        except Exception as e:
            logger.error(f"Login error: {e}")
            return False, "Login failed. Please try again.", None

    @staticmethod
    def get_user(user_id: int) -> Optional[dict]:
        """
        Get user by ID.

        Args:
            user_id: User ID

        Returns:
            User data or None
        """
        db = get_db()
        user = db.execute_query(
            "SELECT * FROM users WHERE id = ?",
            (user_id,),
            fetch_one=True,
        )
        return dict(user) if user else None

    @staticmethod
    def change_password(user_id: int, old_password: str, new_password: str) -> Tuple[bool, str]:
        """
        Change user password.

        Args:
            user_id: User ID
            old_password: Current password
            new_password: New password

        Returns:
            Tuple of (success, message)
        """
        try:
            # Get user
            user = AuthService.get_user(user_id)
            if not user:
                raise AuthenticationError("User not found")

            # Verify old password
            if not AuthService.verify_password(old_password, user['password_hash']):
                raise AuthenticationError("Current password is incorrect")

            # Validate new password
            if len(new_password) < 6:
                raise ValidationError("New password must be at least 6 characters")

            # Update password
            password_hash = AuthService.hash_password(new_password)
            db = get_db()
            db.execute_update(
                "UPDATE users SET password_hash = ? WHERE id = ?",
                (password_hash, user_id),
            )

            logger.info(f"Password changed for user: {user['email']}")
            return True, "Password changed successfully"
        except (AuthenticationError, ValidationError) as e:
            return False, str(e)
        except Exception as e:
            logger.error(f"Password change error: {e}")
            return False, "Password change failed"
