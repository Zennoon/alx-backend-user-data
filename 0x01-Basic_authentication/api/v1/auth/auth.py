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
    """Basic authentication"""
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Require authentication"""
        return False
    
    def authorization_header(self, request=None) -> str:
        """Authorization header"""
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """Current user"""
        return None
