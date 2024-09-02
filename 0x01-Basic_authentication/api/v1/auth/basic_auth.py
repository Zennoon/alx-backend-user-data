#!/usr/bin/env python3
"""
Contains:
    Classes
    =======
    BasicAuth - Inherits from Auth and implements
    basic authentication
"""
import base64
from api.v1.auth.auth import Auth
from typing import Tuple


class BasicAuth(Auth):
    """Implements Basic Authentication"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracts the encoded part of the 'Authorization' header
        value"""
        if authorization_header and isinstance(authorization_header, str):
            if authorization_header.startswith("Basic "):
                return authorization_header[6:]
        return None

    def decode_base64_authorization_header(self,
                                           b64_auth_header: str) -> str:
        """Decodes the base64 encoded authorization header value"""
        if b64_auth_header and isinstance(b64_auth_header, str):
            try:
                b64_decoded = base64.b64decode(b64_auth_header)
            except Exception:
                return None
            return b64_decoded.decode("utf-8")
        return None

    def extract_user_credentials(self,
                                 decoded_b64_auth_header: str) -> Tuple[str, str]:
        """Extract user credentials from decoded Authorization header"""
        if (decoded_b64_auth_header
                and isinstance(decoded_b64_auth_header, str)):
            if ":" in decoded_b64_auth_header:
                email, password = decoded_b64_auth_header.split(":")
                return (email, password)
        return (None, None)
