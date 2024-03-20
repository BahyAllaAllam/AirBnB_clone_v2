#!/usr/bin/python3
"""City Module"""
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")


class City(BaseModel, Base):
    """City (models/city.py):

    Purpose: Represents a city.

    Attributes:
        state_id: string, optional - The ID of the state the city belongs to.
        name: string, optional - The name of the city.

    Usage:
        Create a new instance of City with
            optional parameters to represent different cities."""

    __tablename__ = 'cities'
    if storage_type == 'db':
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey('states.id'), nullable=False)
        places = relationship("Place", backref="cities",
                              cascade="all, delete-orphan")
    else:
        state_id = ""
        name = ""
