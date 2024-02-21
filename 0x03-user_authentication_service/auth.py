#!/usr/bin/env python3
""" Auth Model """
import bcrypt
from db import DB
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound


def _hash_password(password: str) -> bytes:
    """ Create and return a salted hash of the input password """
    password = password.encode()
    return bcrypt.hashpw(password, bcrypt.gensalt())


def _generate_uuid() -> str:
    """
    Create and return a string representation of a new UUID.
    """
    return str(uuid4())


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

    def valid_login(self, email: str, password: str) -> bool:
        """ check if user is register or not """
        try:
            user = self._db.find_user_by(email=email)
            password = password.encode()
            return bcrypt.checkpw(password, user.hashed_password)
        except Exception:
            return False

    def create_session(self, email: str) -> str:
        """ Create, store and return a new session id """
        try:
            session_id = _generate_uuid()
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, session_id=session_id)
        except Exception:
            return None
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """ Get the user by the session_id """
        try:
            user = self._db.find_user_by(session_id=session_id)
        except Exception:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """ updates the corresponding user’s session ID to None. """
        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """ Create, store and return a new reset_token """
        try:
            reset_token = _generate_uuid()
            user = self._db.find_user_by(email=email)
            self._db.update_user(user.id, reset_token=reset_token)
        except Exception:
            raise ValueError
        return reset_token
