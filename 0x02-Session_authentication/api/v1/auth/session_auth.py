#!/usr/bin/env python3
"""
Contains:
    Classes
    =======
    SessionAuth - Session authentication
"""
import uuid
from api.v1.auth.auth import Auth


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
