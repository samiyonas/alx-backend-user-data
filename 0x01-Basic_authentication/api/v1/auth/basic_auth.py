#!/usr/bin/env python3
""" Basic auth """
from api.v1.auth.auth import Auth
from models.user import User
from typing import TypeVar
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
            return (None, None)
        email_password = decoded_base64_authorization_header.split(":")
        if len(email_password) <= 1:
            return (None, None)
        return tuple(email_password)

    def user_object_from_credentials(
            self, user_email: str, user_pwd: str) -> TypeVar('User'):
        """ returns the User instance based on his email and password """
        if not isinstance(user_email, str):
            return None
        if not isinstance(user_pwd, str):
            return None

        user = User()
        user.email = user_email
        user.password = user_pwd

        search_result = user.search({"email": user_email})

        if not search_result:
            return None
        if search_result[0].is_valid_password(user_pwd):
            return search_result[0]
        return None
