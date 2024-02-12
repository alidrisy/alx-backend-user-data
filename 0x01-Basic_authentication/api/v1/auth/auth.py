#!/usr/bin/env python3
""" Model for th object Auth """
from flask import request
from typing import List, TypeVar


class Auth:
    """ Class to Authorized requests """

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Returns True if the path is not in the list of strings
        excluded_paths else returns False """
        if not path or not excluded_paths:
            return True
        path = path if path[-1] == "/" else path + "/"
        return all(path != i for i in excluded_paths)

    def authorization_header(self, request=None) -> str:
        """ Returns None """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Returns None """
        return None
