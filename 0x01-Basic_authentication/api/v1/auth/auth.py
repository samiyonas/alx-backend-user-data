#!/usr/bin/env python3
""" Authentication class """
import requests
from typing import List, TypeVar


class Auth:
    """ the Authentication class """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ returns False """
        if path[len(path) - 1] == '/':
            path1 = path[:len(path) - 1]
        else:
            path1 = path + '/'

        if not path or not excluded_paths:
            return True
        if path in excluded_paths or path1 in excluded_paths:
            return False
        else:
            return True

    def authorization_header(self, request=None) -> str:
        """ returns None """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ return None """
        return None
