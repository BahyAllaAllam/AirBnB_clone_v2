import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
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
        self.__session = sessionmaker(bind=self.__engine)()

    def save(self, obj):
        """Save the object to the database."""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete the object from the database."""
        if obj:
            self.__session.delete(obj)
            self.__session.commit()

    def all(self, cls=None):
        """Query all objects of a specific class from the database."""
        dbobjects = {}
        if cls:
            if type(cls) is str and cls in classes:
                for obj in self.__session.query(classes[cls]).all():
                    key = str(obj.__class__.__name__) + "." + str(obj.id)
                    val = obj
                    dbobjects[key] = val
            elif cls.__name__ in classes:
                for obj in self.__session.query(cls).all():
                    key = str(obj.__class__.__name__) + "." + str(obj.id)
                    val = obj
                    dbobjects[key] = val
        else:
            for k, v in classes.items():
                for obj in self.__session.query(v).all():
                    key = str(v.__name__) + "." + str(obj.id)
                    val = obj
                    dbobjects[key] = val
        return dbobjects

    def new(self, obj):
        """Add the object to the current database session."""
        self.__session.add(obj)

    def delete(self, obj=None):
        if obj:
            self.__session.delete(obj)

    def reload(self):
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(Session)
