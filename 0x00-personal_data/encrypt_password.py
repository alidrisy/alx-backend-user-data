#!/usr/bin/env python3
""" Model for encrypting passwords """
import bcrypt


def hash_password(password: str) -> bytes:
    """returns a salted, hashed password, which is a byte string"""
    password = password.encode()
    return bcrypt.hashpw(password, bcrypt.gensalt())
