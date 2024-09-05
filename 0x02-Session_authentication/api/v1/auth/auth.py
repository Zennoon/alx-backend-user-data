#!/usr/bin/env python3
"""
Contains:
    Classes
    =======
    Auth - An authentication class
"""
import os
from flask import request
from typing import List, TypeVar


class Auth:
    """Template for authentication classes"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require authentication"""
        return (not path
                or not excluded_paths
                or (((path if path.endswith("/") else path + "/")
                    not in excluded_paths)
                    and True not in [
                        ex_path.endswith("*") and path.startswith(ex_path[:-1])
                        for ex_path in excluded_paths
                    ])
                )

    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        if request:
            auth_header = request.headers.get("Authorization")
            if auth_header:
                return auth_header
        return None

    def session_cookie(self, request=None):
        """Get the _my_session_id cookie from given request"""
        if request:
            cookie_name = os.getenv("SESSION_NAME", "_my_session_id")
            return request.cookies.get(cookie_name)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        return None
