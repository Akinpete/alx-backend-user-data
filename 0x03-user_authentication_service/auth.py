#!/usr/bin/env python3
"""Auth module
"""
import bcrypt


def _hash_password(pwd):
    bytes = pwd.encode('utf-8')
    salt = bcrypt.gensalt()
    hash = bcrypt.hashpw(bytes, salt)
    return hash
