#!/usr/bin/env python3
"""Auth module
"""
import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
import uuid
from user import User


def _hash_password(pwd):
    """
    Hashes pw using bcrypt

    Args:
       password
    """
    bytes = pwd.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash


def _generate_uuid():
    """
    return a string representation of a new UUID
    """
    return str(uuid.uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """
    def __init__(self):
        """
        Initialize a new Auth instance
        """
        self._db = DB()

    def register_user(self, email, password):
        """
        Registers a new user if the email doesn't already exist.

        Args:
            email (str): The email of the user to register.
            password (str): The user's password to be hashed and saved.

        Returns:
            User: The newly registered User object.

        Raises:
            ValueError: If a user with the provided email already exists.
        """
        try:
            self._db.find_user_by(email=email)
            raise ValueError("User {} already exists.".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            new_user = self._db.add_user(email=email,
                                         hashed_password=hashed_password)
            return new_user

    def valid_login(self, email, password):
        """
        Verifies if the provided password matches the stored hash for the user.

        Args:
            email (str): User's email address.
            password (str): User's plaintext password to verify.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode('utf-8'), user.hashed_password):
                return True
            return False
        except NoResultFound as e:
            return False

    def create_session(self, email: str) -> str:
        """
        Creates a new session for the user and returns the session ID.
        """
        session_id = _generate_uuid()
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except Exception as e:
            print(e)

    def get_user_from_session_id(self, session_id):
        """
        find user by session ID
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id):
        """
        Updates the session_id of the user to None to log out the session.

        Args:
            user_id (int): The ID of the user whose session will be destroyed.

        Returns:
            None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user_id=user_id, session_id=None)
            return None
        except NoResultFound:
            print(f"User with id {user_id} not found")
        except Exception as e:
            print(e)

    def get_reset_password_token(self, email):
        """
        Generate reset password token
        """
        reset_token = str(uuid.uuid4())
        try:
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, reset_token=reset_token)
            return reset_token
        except NoResultFound:
            raise ValueError("User not found!")
