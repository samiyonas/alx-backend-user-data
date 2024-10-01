#!/usr/bin/env python3
""" Authentication class """
import requests
from typing import List, TypeVar


class Auth:
    """ the Authentication class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns False """
        return False

    def authorization_header(self, request=None) -> str:
        """ returns None """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ return None """
        return None
