#!/usr/bin/env python3
""" Model for th object SessionExpAuth """
from api.v1.auth.session_auth import SessionAuth
from os import getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """ Class to Authorized sessions that inherits from SessionAuth """

    def __init__(self):
        """ Initilaize data """
        try:
            self.session_duration = int(getenv("SESSION_DURATION", "0"))
        except Exception:
            self.session_duration = 0

    def create_session(self, user_id: str = None) -> str:
        """ Creates a Session ID for a user_id """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        session_dictionary = {"user_id": user_id, "created_at": datetime.now()}
        self.user_id_by_session_id[session_id] = session_dictionary
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Returns a User ID based on a Session ID """
        if type(session_id) != str:
            return None

        session_dictionary = self.user_id_by_session_id.get(session_id)
        if session_dictionary is None:
            return None
        if self.session_duration < 1:
            return session_dictionary.get("user_id")
        if "created_at" not in session_dictionary.keys():
            return None
        crAt = session_dictionary.get("created_at")
        cr = timedelta(days=crAt.day, seconds=crAt.second, microseconds=0,
                       milliseconds=0, minutes=crAt.minute, hours=crAt.hour)
        now = timedelta(days=datetime.now().day, seconds=datetime.now().second,
                        microseconds=0, milliseconds=0,
                        minutes=datetime.now().minute,
                        hours=datetime.now().hour)
        if cr.total_seconds() + self.session_duration < now.total_seconds():
            return None
        return session_dictionary.get("user_id")
