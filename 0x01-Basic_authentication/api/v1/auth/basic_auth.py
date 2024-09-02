#!/usr/bin/env python3
"""
Contains:
    Classes
    =======
    BasicAuth - Inherits from Auth and implements
    basic authentication
"""
import base64
import hashlib
from api.v1.auth.auth import Auth
from models.user import User
from typing import Tuple, TypeVar


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
                                 decoded_b64_auth_hdr: str) -> Tuple[str, str]:
        """Extract user credentials from decoded Authorization header"""
        if (decoded_b64_auth_hdr
                and isinstance(decoded_b64_auth_hdr, str)):
            if ":" in decoded_b64_auth_hdr:
                email, password = decoded_b64_auth_hdr.split(":")
                return (email, password)
        return (None, None)

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """Retrieves a User object from the given email and password"""
        if (user_email and isinstance(user_email, str)
                and user_pwd and isinstance(user_pwd, str)):
            try:
                users = User.search({
                    "email": user_email
                })
            except Exception:
                return None
            if users:
                user = users[0]
                hashed_pwd = hashlib.sha256(
                    user_pwd.encode()
                ).hexdigest().lower()
                if user.password == hashed_pwd:
                    return user
        return None
    
    def current_user(self, request=None) -> TypeVar("User"):
        """Returns the current user (who issued the request)"""
        auth_header = self.authorization_header(request)
        b64_encoded = self.extract_base64_authorization_header(auth_header)
        b64_decoded = self.decode_base64_authorization_header(b64_encoded)
        print(b64_decoded)
        user_email, user_pwd = self.extract_user_credentials(b64_decoded)
        user = self.user_object_from_credentials(user_email, user_pwd)
        return user
