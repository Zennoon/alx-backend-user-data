#!/usr/bin/env python3
"""
Contains:
    Classes
    =======
    SessionAuth - Session authentication
"""
import uuid

from api.v1.auth.auth import Auth
from models.user import User


class SessionAuth(Auth):
    """Implements session authentication"""
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a new session for users"""
        if user_id and isinstance(user_id, str):
            session_id = str(uuid.uuid4())
            self.user_id_by_session_id[session_id] = user_id
            return session_id
        return None

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Retrieves user id associated with given session id"""
        if session_id and isinstance(session_id, str):
            return self.user_id_by_session_id.get(session_id)
        return None

    def current_user(self, request=None):
        """Returns the current user issuing the request
        (if they are authenticated)"""
        cookie = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie)
        return User.get(user_id)
