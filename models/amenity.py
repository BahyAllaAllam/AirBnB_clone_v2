#!/usr/bin/python3
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Table
from sqlalchemy.orm import relationship
from os import getenv

storage_type = getenv("HBNB_TYPE_STORAGE")


class Amenity(BaseModel, Base):
    """Amenity (models/amenity.py):

    Purpose: Represents an amenity.

    Attributes:
        name: string, optional - The name of the amenity.

    Usage:
        Create a new instance of Amenity with
            optional parameters to represent different amenities."""

    __tablename__ = 'amenities'
    if storage_type == 'db':
        from models.place import place_amenity
        name = Column(String(128), nullable=False)
        place_amenities = relationship("Place", secondary=place_amenity,
                                       back_populates="amenities")
    else:
        name = ""
