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
from typing import Union

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

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """Returns the user associated with a session id"""
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id) -> None:
        """Destroys the session of user with given id"""
        try:
            self._db.update_user(user_id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """Generates a reset token for user with given email"""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError
        self._db.update_user(user.id, reset_token=_generate_uuid())
        return user.reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates a user's password
        Args:
            reset_token (str): reset_token issued to reset the password
            password (str): user's new password
        Return:
            None
        """
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError()

        hashed = _hash_password(password)
        self._db.update_user(user.id, hashed_password=hashed, reset_token=None)
