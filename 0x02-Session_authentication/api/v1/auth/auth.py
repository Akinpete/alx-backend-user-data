#!/usr/bin/env python3
"""
Auth management for the API
"""
from typing import List, TypeVar
from flask import request
from os import getenv


class Auth:
    """
    Base API Auth management class
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines whether a given path requires authentication or not
        Args:
            - path(str): Url path to be checked
            - excluded_paths(List of str): List of paths that do not require
              authentication
        Return:
            - True if path is not in excluded_paths, else False
        """
        # Step 1: Return True if path is None
        if path is None:
            return True

        # Step 2: Return True if excluded_paths is None or empty
        if excluded_paths is None or len(excluded_paths) == 0:
            return True

        # Normalize the path by removing trailing slashes
        normalized_path = path.rstrip('/')

        # Step 3: Loop through excluded_paths and
        # check if normalized path matches
        for excluded_path in excluded_paths:
            normalized_excluded_path = excluded_path.rstrip('/')
            if normalized_path == normalized_excluded_path:
                return False
            # Check for wildcard match
            if normalized_excluded_path.endswith('*'):
                # Remove '/*' from the end
                if normalized_path.startswith(normalized_excluded_path[:-1]):
                    return False

        # If no match found, return True (authentication required)
        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from a request object
        """
        if request is None:
            return None
        header = request.headers.get('Authorization')
        if header is None:
            return None
        return header

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns a User instance from information from a request object
        """
        return None

    def session_cookie(self, request=None):
        """
        Returns a cookie value from a request
        Args:
            request : request object
        Return:
            value of _my_session_id cookie from request object
        """
        if request is None:
            return None
        session_name = getenv('SESSION_NAME')
        return request.cookies.get(session_name)
