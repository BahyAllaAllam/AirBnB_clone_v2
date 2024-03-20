#!/usr/bin/python3
"""User module"""
from models.base_model import BaseModel, Base
import os
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel):
    """
    User class inherits from BaseModel.
    Public class attributes:
        email: string - empty string
        password: string - empty string
        first_name: string - empty string
        last_name: string - empty string
    """
    __tablename__ = 'users'
    if storage_type == 'db':
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship(
            'Place',
            cascade="all, delete, delete-orphan",
            backref='user'
        )
        reviews = relationship(
            'Review',
            cascade="all, delete, delete-orphan",
            backref='user'
        )
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """Initialize User instance."""
        super().__init__(*args, **kwargs)
