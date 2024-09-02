#!/usr/bin/env python3
"""
Contains:
    Classes
    =======
    Auth - An authentication class
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Template for authentication classes"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require authentication"""
        return (not path
                or not excluded_paths
                or (path if path.endswith("/") else path + "/")
                not in excluded_paths)

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        if request:
            auth_header = request.headers.get("Authorization")
            if auth_header:
                return auth_header
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        return None


class BasicAuth(Auth):
    """Implements Basic Authentication"""
    pass
