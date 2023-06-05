#!/usr/bin/env python3
"""method hashes a pwssawword from str args to bytes"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """hashes the pwd
    hashes a salted hash of the pwd"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password
