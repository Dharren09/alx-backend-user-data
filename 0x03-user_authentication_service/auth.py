#!/usr/bin/env python3
"""method hashes a pwssawword from str args to bytes"""

import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """hashes the pwd
    hashes a salted hash of the pwd"""
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def _generate_uuid() -> str:
    """returns a str rep of a new uuid"""
    return str(uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """initializes new auth instance"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """registers a new user to the database"""
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))

    def valid_login(self, email, password) -> bool:
        """checks if users login creditials are authentic"""
        user = None
        try:
            user = self._db.find_user_by(email=email)
            if user is not None:
                return bcrypt.checkpw(password.encode("utf-8"),
                                      user.hashed_password)
        except NoResultFound:
            return False
        return False
