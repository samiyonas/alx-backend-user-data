#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from user import Base
from user import User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """ add user to the user table """
        new_user = User(email=email, hashed_password=hashed_password)
        sesh = self._session
        sesh.add(new_user)
        sesh.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """ search for user """
        for key in kwargs:
            if key not in User.__table__.columns:
                raise InvalidRequestError()

        session = self._session
        found_user = session.query(User).filter_by(**kwargs).first()
        if not found_user:
            raise NoResultFound()
        else:
            return found_user

    def update_user(self, user_id: int, **kwargs) -> None:
        """ update user """
        session = self._session
        user = self.find_user_by(id=user_id)
        for key, value in kwargs.items():
            if key in User.__table__.columns:
                user.key = value
            else:
                raise ValueError()

        session.commit()
        return None
