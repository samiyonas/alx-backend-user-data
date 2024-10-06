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

    def get_user_from_session_id(self, session_id: str) -> Union[User, None):
        """ get a user from a session id """
        if not session_id:
            return None
        try:
            new_user = self._db.find_user_by(session_id=session_id)
            return new_user
        except NoResultFound:
            return None
