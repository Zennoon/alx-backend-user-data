#!/usr/bin/env python3
"""
Contains:
    Functions
    =========
    _hash_password - Accepts a string and hashes it
    using the bcrypt.hashpw function
"""
import bcrypt
import uuid
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


def _generate_uuid() -> str:
    return str(uuid.uuid4())


class Auth:
    """
    Auth class to interact with the authentication database.
    """
    def __init__(self):
        """Initialize a new instance of the Auth class"""
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

    def valid_login(self, email: str, password: str) -> bool:
        """Checks if the credentials for login are correct/valid"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False
        return bcrypt.checkpw(password.encode("utf-8"), user.hashed_password)

    def create_session(self, email: str) -> str:
        """Creates session & session id for user"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None
        self._db.update_user(user.id, session_id=_generate_uuid())
        return user.session_id
