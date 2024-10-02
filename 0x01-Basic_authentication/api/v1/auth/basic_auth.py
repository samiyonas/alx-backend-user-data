#!/usr/bin/env python3
""" Basic auth """
from api.v1.auth.auth import Auth
import base64


class BasicAuth(Auth):
    """ Basic Authentication """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """ returns the Base64 part of the Authorization """
        standard = "Basic "
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header or len(authorization_header) <= 6:
            return None
        if authorization_header[:6] != standard:
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
            self, base64_authorization_header: str) -> str:
        """ returns the decoded value of Base64 string """
        if not isinstance(base64_authorization_header, str):
            return None
        try:
            to_byte = base64.b64decode(base64_authorization_header)
            return to_byte.decode("utf-8")
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """ return the user email and password from Base64 decoded value """
        if not isinstance(decoded_base64_authorization_header, str):
            return None
        email_password = decoded_base64_authorization_header.split(":")
        if len(email_password) <= 1:
            return None
        return tuple(email_password)
