#!/usr/bin/python3

import json


class FileStorage:
    """
    FileStorage class handles the serialization and
        deserialization of instances to/from a JSON file.
    """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """
        Returns the dictionary of all objects.
        """
        if cls is not None:
            filtered_objects = {}
            for key, obj in self.__objects.items():
                if type(obj).__name__ == cls.__name__:
                    filtered_objects[key] = obj
            return filtered_objects
        return FileStorage.__objects

    def new(self, obj):
        """
        Adds a new object to the __objects dictionary.
        """
        key = "{}.{}".format(type(obj).__name__, obj.id)
        FileStorage.__objects[key] = obj

    def save(self):
        """
        Serializes __objects to JSON and saves it to the file.
        """
        serialized_objects = {}
        for key, value in FileStorage.__objects.items():
            serialized_objects[key] = value.to_dict()
        with open(FileStorage.__file_path, "w") as f:
            json.dump(serialized_objects, f)

    def reload(self):
        """
        Deserializes JSON file to __objects dictionary.
        """
        try:
            with open(FileStorage.__file_path, "r") as f:
                data = json.load(f)
            from models import (
                BaseModel, User, State, City, Amenity, Place, Review
            )
            for key, value in data.items():
                class_name, obj_id = key.split('.')
                cls = eval(class_name)
                instance = cls(**value)
                FileStorage.__objects[key] = instance
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """ Deletes obj from __objects if it exists
        """
        if obj is not None:
            key = "{}.{}".format(type(obj).__name__, obj.id)
            if key in self.__objects:
                del self.__objects[key]
