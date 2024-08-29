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
