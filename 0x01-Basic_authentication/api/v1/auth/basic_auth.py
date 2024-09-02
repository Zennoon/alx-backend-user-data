#!/usr/bin/env python3
"""
Contains:
    Classes
    =======
    BasicAuth - Inherits from Auth and implements
    basic authentication
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """Implements Basic Authentication"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracts the encoded part of the 'Authorization' header
        value"""
        if authorization_header and isinstance(authorization_header, str):
            if authorization_header.startswith("Basic "):
                return authorization_header.removeprefix("Basic ")
        return None
