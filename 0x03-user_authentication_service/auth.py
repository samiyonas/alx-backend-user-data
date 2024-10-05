#!/usr/bin/env python3
""" Authentication goes here """
import bcrypt


def _hash_password(password: str) -> bytes:
    """ returns hashed password in bytes """
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_pwd
