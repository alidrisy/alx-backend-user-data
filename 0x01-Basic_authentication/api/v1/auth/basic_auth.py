#!/usr/bin/env python3
""" Model for th object BasicAuth """
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
import base64


class BasicAuth(Auth):
    """ Class to Authorized requests that inherits from Auth """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Returns the Base64 part of the Authorization header for
            a Basic Authentication """
        if not authorization_header or type(authorization_header) is not str:
            return None
        if authorization_header[:6] != "Basic ":
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(self, base64_authorization_header:
                                           str) -> str:
        """ Returns the decoded value of a Base64 string
            base64_authorization_header """
        try:
            author = base64.b64decode(base64_authorization_header)
            return author.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(self, decoded_base64_authorization_header:
                                 str) -> (str, str):
        """
        Returns the user email and password from the Base64 decoded value.
        """
        try:
            info = decoded_base64_authorization_header.split(":", 1)
            return tuple(info) if len(info) == 2 else (None, None)
        except Exception:
            return (None, None)

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ Returns the User instance based on his email and password """
        if type(user_email) is str or type(user_pwd) is str:
            try:
                users = User.search({"email": user_email})
            except Exception:
                return None
            if len(users) <= 0:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
        return None
    
    def current_user(self, request=None) -> TypeVar('User'):
        """ Overloads Auth and retrieves the User instance for a request """
        authorization = self.authorization_header(request)
        auth = self.extract_base64_authorization_header(authorization)
        decode_auth = self.decode_base64_authorization_header(auth)
        tuple_auth = self.extract_user_credentials(decode_auth)
        return self.user_object_from_credentials(tuple_auth[0], tuple_auth[1])
