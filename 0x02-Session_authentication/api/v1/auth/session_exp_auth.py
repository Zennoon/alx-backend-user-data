#!/usr/bin/env python3
"""
Contains:
    Classes
    =======
    SessionExpAuth - Session authentication with expiration
"""
from datetime import datetime, timedelta
import os

from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """Session authentication with expiration"""
    def __init__(self):
        """Initializes an instance"""
        self.session_duration = os.getenv("SESSION_DURATION", 0)
        try:
            self.session_duration = int(self.session_duration)
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Creates a session for user with given ID"""
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {
                "user_id": user_id,
                "created_at": datetime.now()
            }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Returns the user id associated with given session id"""
        if session_id:
            user_session_dct = self.user_id_by_session_id.get(session_id)
            if user_session_dct:
                created_at = user_session_dct.get("created_at")
                if created_at:
                    td = created_at + timedelta(seconds=self.session_duration)
                    if (self.session_duration <= 0
                            or datetime.now() <= td):
                        return user_session_dct.get("user_id")
        return None
