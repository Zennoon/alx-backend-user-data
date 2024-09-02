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
        return False
    
    def authorization_header(self, request=None) -> str:
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        return None


a = Auth()

print(a.require_auth("/api/v1/status/", ["/api/v1/status/"]))
print(a.authorization_header())
print(a.current_user())