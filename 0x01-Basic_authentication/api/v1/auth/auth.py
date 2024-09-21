#!/usr/bin/env python3
"""
Auth management for the API
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """
    API Auth management class
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
        return False

    def authorization_header(self, request=None) -> str:
        """
        Returns the authorization header from a request object
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns a User instance from information from a request object
        """
        return None
