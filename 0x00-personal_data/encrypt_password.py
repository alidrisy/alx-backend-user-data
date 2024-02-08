#!/usr/bin/env python3
""" Model for encrypting passwords """
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password, which is a byte string"""
    password = password.encode()
    return bcrypt.hashpw(password, bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """validate that the provided password matches the hashed password."""
    password = password.encode()
    if bcrypt.checkpw(password, hashed_password):
        return True
    return False
