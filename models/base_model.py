#!/usr/bin/python3
"""
BaseModel class represents the base model for other classes in the project.
"""

from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid
from datetime import datetime
import models

Base = declarative_base()


class BaseModel:
    """
    BaseModel class represents the base model for other classes in the project.
    It defines common attributes and methods,
        that are inherited by other classes.

    Attributes:
        id (str): Unique identifier for each instance,
                    generated using uuid.uuid4().
        created_at (datetime): Date and time when the instance is created.
        updated_at (datetime):
                    Date and time when the instance is last updated.
    """

    id = Column(String(60), primary_key=True, nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow())
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """
        Initializes a new instance of the BaseModel class.
        It assigns a unique id, and sets the created_at and updated_at
            attributes to the current datetime.
        If kwargs is not empty, it sets the instance attributes
            using the provided dictionary.
        Otherwise, it assigns a unique id, and sets the created_at and
            updated_at attributes to the current datetime.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
        """
        if kwargs:
            for key, value in kwargs.items():
                if key != '__class__':
                    setattr(self, key, value)
            if 'created_at' in kwargs:
                self.created_at = datetime.strptime(
                    kwargs['created_at'], "%Y-%m-%dT%H:%M:%S.%f"
                )
            if 'updated_at' in kwargs:
                self.updated_at = datetime.strptime(
                    kwargs['updated_at'], "%Y-%m-%dT%H:%M:%S.%f"
                )
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()

    def __str__(self):
        """
        Returns a string representation of the BaseModel instance.

        Returns:
            str: A string containing the class name, id,
                 and dictionary representation of the instance.
        """
        return "[{}] ({}) {}".format(
            type(self).__name__, self.id, self.__dict__
        )

    def save(self):
        """
        Updates the updated_at attribute with the current datetime.
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """
        Returns:
            dict: A dictionary containing all attributes of the instance along
                  with class name, created_at,
                  and updated_at converted to ISO format.
        """
        obj_dict = self.__dict__.copy()
        obj_dict['__class__'] = type(self).__name__
        obj_dict['created_at'] = self.created_at.isoformat()
        obj_dict['updated_at'] = self.updated_at.isoformat()
        obj_dict.pop('_sa_instance_state', None)
        return obj_dict

    def delete(self):
        """Deletes this BaseModel instance from the storage"""
        models.storage.delete(self)
