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
