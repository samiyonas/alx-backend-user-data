#!/usr/bin/env python3
""" User model (database) """
from sqlalchemy import (
        Column,
        String,
        Integer)
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class User(Base):
    """ this is the user database model """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    session_id = Column(String, nullable=True)
    reset_token = Column(String, nullable=True)
