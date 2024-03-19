#!/usr/bin/python3
import os

from .base_model import BaseModel
from .user import User
from .state import State
from .city import City
from .amenity import Amenity
from .place import Place
from .review import Review

# Determine storage type based on environment variable or configuration
storage_type = os.getenv('HBNB_TYPE_STORAGE')

if storage_type == 'db':
    from .engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from .engine.file_storage import FileStorage
    storage = FileStorage()
storage.reload()
