#!/usr/bin/python3
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from models.engine.file_storage import FileStorage
from models import storage_type


class State(BaseModel):
    """State (models/state.py):

    Purpose: Represents a state.

    Attributes:
        name: string, optional - The name of the state.

    Usage:
        Create a new instance of State with
            optional parameters to represent different states."""

    __tablename__ = 'states'
    if storage_type == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state",
                              cascade="all, delete-orphan")
    else:
        name = ""

        @property
        def cities(self):
            cities_list = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    cities_list.append(city)
            return cities_list
