#!/usr/bin/env python3
"""
Contains:
    Classes
    =======
    User - An SQLAlchemy mapping model to the database table 'users'
"""
from sqlalchemy import (
    Column,
    Integer,
    String
)
from sqlalchemy.orm import declarative_base

base = declarative_base()


class User(base):
    """Mapping model to the users table of the connected database"""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)
