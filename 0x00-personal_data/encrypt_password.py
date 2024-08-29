#!/usr/bin/env python3
"""
Contains:
    Functions
    =========
    hash_password - Hashes given strings (passwords) using bcrypt
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """Generates a salted hash for the given password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """Checks if the given password matched against the hash"""
    return bcrypt.checkpw(password.encode(), hashed_password)
