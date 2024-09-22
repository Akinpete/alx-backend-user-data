#!/usr/bin/env python3
"""
BasicAuth management for the API
"""
from typing import List, TypeVar
from flask import request
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    Basic API Auth management class
    """
    pass
