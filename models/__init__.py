#!/usr/bin/python3
"""The instantiates"""
from os import getenv

from .base_model import BaseModel
from .user import User
from .state import State
from .city import City
from .amenity import Amenity
from .place import Place
from .review import Review

# Determine storage type based on environment variable or configuration
if getenv('HBNB_TYPE_STORAGE') == 'db':
    from .engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from .engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
