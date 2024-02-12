#!/usr/bin/env python3
""" Model for th object BasicAuth """
from api.v1.auth.auth import Auth
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
