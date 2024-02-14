#!/usr/bin/env python3
""" Model for th object Auth """
from typing import List, TypeVar
from os import getenv


class Auth:
    """ Class to Authorized requests """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns True if the path is not in the list of strings
        excluded_paths else returns False """
        if not path or not excluded_paths:
            return True
        path = path if path[-1] == "/" else path + "/"
        for i in excluded_paths:
            if path == i:
                return False
            if i[-1] == "*":
                s = len(i) - 1
                if i[:s] == path[:s]:
                    return False
        return True

    def authorization_header(self, request=None) -> str:
        """ Returns the value of the header request Authorization or None """
        if request:
            return request.headers.get("Authorization", None)
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns None """
        return None

    def session_cookie(self, request=None):
        """ Returns a cookie value from a request """
        if request is None:
            return None
        _my_session_id = getenv("SESSION_NAME")
        if _my_session_id:
            return request.cookies.get(_my_session_id)
        return None

