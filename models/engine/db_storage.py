#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone."""
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import BaseModel, Base
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State

classes = {"BaseModel": BaseModel, "State": State, "City": City, "User": User,
           "Place": Place, "Review": Review, "Amenity": Amenity}


class DBStorage:
    """Manages storage of hbnb models in a SQL database."""
    __engine = None
    __session = None

    def __init__(self):
        """Connect to the MySQL database."""
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            os.getenv('HBNB_MYSQL_USER'),
            os.getenv('HBNB_MYSQL_PWD'),
            os.getenv('HBNB_MYSQL_HOST'),
            os.getenv('HBNB_MYSQL_DB'),
            pool_pre_ping=True))
        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def reload(self):
        """Reload data from the database."""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()

    def save(self):
        """Save the object to the database."""
        self.__session.commit()

    def all(self, cls=None):
        """Query all objects of a specific class from the database."""
        all_objs = {}
        objs = None
        if cls and isinstance(cls, str) and cls in classes:
            objs = self.__session.query(classes[cls]).all()
            for obj in objs:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                all_objs[key] = obj
        elif cls and not isinstance(cls, str) and cls.__name__ in classes:
            objs = self.__session.query(cls).all()
            for obj in objs:
                key = "{}.{}".format(type(obj).__name__, obj.id)
                all_objs[key] = obj
        else:
            for value in classes.values():
                for obj in self.__session.query(value).all():
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    all_objs[key] = obj

        return all_objs

    def new(self, obj):
        """Add the object to the current database session."""
        if obj:
            self.__session.add(obj)

    def delete(self, obj=None):
        """Delete the object to the current database session."""
        if obj:
            self.__session.delete(obj)

    def close(self):
        """close session"""
        self.__session.close()
