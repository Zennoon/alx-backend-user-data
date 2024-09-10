#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db")
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """Creates and adds a new user to the database"""
        user = User()
        session = self._session
        user.email = email
        user.hashed_password = hashed_password
        session.add(user)
        session.commit()
        return user

    def find_user_by(self, *args, **kwargs):
        """
        Filters users by given keyword args and returns result
        if found, else raise an exception
        """
        users = self._session.query(User)
        for key, val in kwargs.items():
            users = users.filter(User.__dict__.get(key) == val)
        return users.one()
