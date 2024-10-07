#!/usr/bin/env python3
""" Authentication goes here """
import bcrypt
from typing import Union
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
from uuid import uuid4


def _hash_password(password: str) -> bytes:
    """ returns hashed password in bytes """
    hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    return hashed_pwd


def _generate_uuid() -> str:
    """ generate ID """
    Id = str(uuid4())
    return Id


class Auth:
    """Auth class to interact with the authentication database
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """ registers user """
        try:
            user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            passwd = _hash_password(password)

            passwd = passwd.decode('utf-8')

            new_user = self._db.add_user(email=email, hashed_password=passwd)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """ check the validity of a login """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        db_passwd = user.hashed_password.encode('utf-8')
        password = password.encode('utf-8')

        if bcrypt.checkpw(password, db_passwd):
            return True
        else:
            return False

    def create_session(self, email: str) -> str:
        """ create a session and return it """
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return None

        UUID = _generate_uuid()
        user.session_id = UUID

        return user.session_id

    def get_user_from_session_id(self, session_id: str) -> Union[str, None]:
        """It takes a single session_id string argument
        Returns a string or None
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None

        return user

    def destroy_session(self, user_id: int) -> None:
        """ destroy a session """
        user = self._db.find_user_by(id=user_id)
        user.session_id = None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """ reset password token """
        user = self._db.find_user_by(email=email)
        if not user:
            raise ValueError()
        UUID = _generate_uuid()
        user.reset_token = UUID
        return UUID
