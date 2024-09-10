#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from typing import Dict, List

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

    def find_user_by(self, **kwargs) -> User:
        """
        Filters users by given keyword args and returns result
        if found, else raise an exception
        """
        users = self._session.query(User)
        return users.filter_by(**kwargs).one()

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update user of given user id with the attribute name
        and values found in kwargs
        """
        user = self.find_user_by(id=user_id)
        for key, val in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, val)
            else:
                raise ValueError
        self._session.add(user)
        self._session.commit()
