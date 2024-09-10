#!/usr/bin/env python3
"""
Contains:
    Functions
    =========
    _hash_password - Accepts a string and hashes it
    using the bcrypt.hashpw function
"""
import bcrypt
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """
    def __init__(self):
        """Initialize a new instance"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Registers a new user into the database after configurations
        and checks are performed
        """
        try:
            _ = self._db.find_user_by(email=email)
        except NoResultFound:
            hashed_pwd = _hash_password(password)
            return self._db.add_user(email, hashed_pwd)
        else:
            raise ValueError("User {} already exists".format(email))
