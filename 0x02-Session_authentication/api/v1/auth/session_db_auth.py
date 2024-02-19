#!/usr/bin/env python3
""" Model for th object SessionDBAuth """
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from uuid import uuid4
from datetime import timedelta


class SessionDBAuth(SessionExpAuth):
    """ Class SessionDBAuth """

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user_id """
        if type(user_id) != str:
            return None

        session_id = str(uuid4())
        user = UserSession(user_id=user_id, session_id=session_id)
        user.save()
        return user.session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns a User ID based on a Session ID """
        if type(session_id) != str:
            return None
        try:
            UserSession.load_from_file()
            user_sessions = UserSession.search({"session_id": session_id})
            user_session = user_sessions[0]
        except Exception:
            return None
        crAt = user_session.created_at
        nowDate = crAt.utcnow()
        cr = timedelta(days=crAt.day, seconds=crAt.second, microseconds=0,
                       milliseconds=0, minutes=crAt.minute, hours=crAt.hour)
        now = timedelta(days=nowDate.day, seconds=nowDate.second,
                        microseconds=0, milliseconds=0,
                        minutes=nowDate.minute,
                        hours=nowDate.hour)
        if cr.total_seconds() + self.session_duration < now.total_seconds():
            user_session.remove()
            return None
        return user_session.user_id

    def destroy_session(self, request=None):
        """ Deletes the user session / logout """
        if request is None:
            return False
        session_id = self.session_cookie(request)
        try:
            user_sessions = UserSession.search({"session_id": session_id})
            user_session = user_sessions[0]
        except Exception:
            return False
        user_session.remove()
        return True
