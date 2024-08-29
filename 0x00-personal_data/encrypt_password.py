#!/usr/bin/env python3
"""
Contains:
    Functions
    =========
    hash_password - Hashes given strings (passwords) using bcrypt
"""
import bcrypt


def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
