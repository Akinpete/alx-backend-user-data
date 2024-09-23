#!/usr/bin/env python3
"""
BasicAuth management for the API
"""
from typing import List, TypeVar
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class SessionAuth(Auth):
    """
    API Auth via Session Auth
    """
    pass
