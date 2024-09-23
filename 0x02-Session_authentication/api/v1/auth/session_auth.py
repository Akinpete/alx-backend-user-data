#!/usr/bin/env python3
"""
BasicAuth management for the API
"""
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User
import uuid


class SessionAuth(Auth):
    """
    API Auth via Session Auth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        creates a Session ID for a user_id
        Args:
            user_id (str): The ID of the user for whom to create a session.

        Returns:
            str: The generated session ID or None if user_id is invalid.
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())

        # Store the session ID with the user_id in the dictionary
        self.user_id_by_session_id[session_id] = user_id

        # Return the session ID
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        retrives a User_id for a Session ID
        Args:
            session_id (str): The sessionID of the user
            for whom to create a session.

        Returns:
            str: The user ID or None if session_id is invalid.
        """
        if session_id is None or not isinstance(session_id, str):
            return None
        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """
        Return a user instance based on a cookie value
        Args:
            request : request object containing cookie
        Return:
            User instance
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)
        user = User.get(user_id)
        return user

    def destroy_session(self, request=None):
        """
        destroy a Session
        Args:
            request: DELETE request

        Returns:
            bool: True
        """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        user = self.user_id_for_session_id(session_id)
        if session_id is None:
            return False
        if user is None:
            return False
        self.user_id_by_session_id.pop(session_id)
        return True
