#!/usr/bin/env python3
""" Auth Model """
import bcrypt
from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ Create and return a salted hash of the input password """
    password = password.encode()
    return bcrypt.hashpw(password, bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Initialize a new DB instance
        """
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ Create and return the User object """
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            password = _hash_password(password)
            return self._db.add_user(email, password)
