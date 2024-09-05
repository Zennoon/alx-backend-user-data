#!/usr/bin/env python3
"""
Contains:
    Classes
    =======
    SessionDBAuth - Session authentication with sessions stored in
    a database
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Session authentication with database"""
    def create_session(self, user_id=None):
        """Creates session and stores it in a database"""
        session_id = super().create_session(user_id)
        if session_id:
            session = UserSession(user_id=user_id, session_id=session_id)
            session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Returns the user id associated with the given
        session id
        """
        if super().user_id_for_session_id(session_id):
            try:
                sessions = UserSession.search({"session_id": session_id})
            except Exception:
                return None
            if sessions:
                return sessions[0].user_id
        return None

    def destroy_session(self, request=None):
        """Removes a session from the database"""
        if request:
            session_id = self.session_cookie(request)
            if session_id:
                user_id = self.user_id_for_session_id(session_id)
                if user_id:
                    try:
                        sessions = UserSession.search({"session_id": session_id})
                    except Exception:
                        return False
                    if sessions:
                        sessions[0].remove()
                        return True
        return False

