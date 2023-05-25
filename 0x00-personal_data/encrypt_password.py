#!/usr/bin/env python3
"""implements a hash function that expects a str arg
and returns a salted, hashed pwd which is a byte"""

import bcrypt


def hash_password(password: str) -> bytes:
    """generate a salt"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), salt)

    return hashed_password
