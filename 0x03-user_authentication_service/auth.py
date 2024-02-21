#!/usr/bin/env python3
""" Model auth for _hash_password function """
import bcrypt


def _hash_password(password: str) -> bytes:
    """ Create and return a salted hash of the input password """
    password = password.encode()
    return bcrypt.hashpw(password, bcrypt.gensalt())
