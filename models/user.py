#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from hashlib import md5


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if 'password' in kwargs:
            kwargs['_password'] = self._hash_password(kwargs['password'])
            del kwargs['password']
        super().__init__(*args, **kwargs)

    @staticmethod
    def _hash_password(password):
        """Hashes password using MD5"""
        return md5(password.encode()).hexdigest()

    @property
    def password(self):
        """Getter for password (not accessible)"""
        return self._password

    @password.setter
    def password(self, pwd):
        """Setter for password - hashes before saving"""
        self._password = self._hash_password(pwd)
