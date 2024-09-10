#!/usr/bin/env python3
"""
Contains:
    Functions
    =========
    _hash_password - Accepts a string and hashes it
    using the bcrypt.hashpw function
"""
import bcrypt


def _hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
