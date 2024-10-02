#!/usr/bin/env python3
""" Basic auth """
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ Basic Authentication """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ returns the Base64 part of the Authorization """
        standard = "Basic "
        if not authorization_header or len(authorization_header) <= 6:
            return None
        if type(authorization_header) != str:
            return None
        if authorization_header[:6] != standard:
            return None
        return authorization_header[6:]
