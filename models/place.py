#!/usr/bin/python3
"""Place module"""
from models.base_model import BaseModel, Base
from sqlalchemy import Table, Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv
import models

storage_type = getenv("HBNB_TYPE_STORAGE")

if storage_type == 'db':
    place_amenity = Table("place_amenity", Base.metadata,
                          Column('place_id', String(60),
                                 ForeignKey('places.id'),
                                 nullable=False, primary_key=True),
                          Column('amenity_id', String(60),
                                 ForeignKey('amenities.id'),
                                 nullable=False, primary_key=True))


class Place(BaseModel, Base):
    """Place (models/place.py):

    Purpose: Represents a place.

    Attributes:
        city_id: string, optional -
            The ID of the city the place is located in.
        user_id: string, optional - The ID of the user who owns the place.
        name: string, optional - The name of the place.
        description: string, optional - Description of the place.
        number_rooms: int, optional - Number of rooms in the place.
        number_bathrooms: int, optional - Number of bathrooms in the place.
        max_guest: int, optional -
            Maximum number of guests allowed in the place.
        price_by_night: int, optional - Price per night for the place.
        latitude: float, optional - Latitude coordinate of the place.
        longitude: float, optional - Longitude coordinate of the place.
        amenity_ids: list of strings, optional -
            List of IDs of amenities available in the place.

    Usage:
        Create a new instance of Place with
            optional parameters to represent different places."""

    __tablename__ = 'places'
    if storage_type == 'db':
        city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
        user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, nullable=False, default=0)
        number_bathrooms = Column(Integer, nullable=False, default=0)
        max_guest = Column(Integer, nullable=False, default=0)
        price_by_night = Column(Integer, nullable=False, default=0)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        amenity_ids = []

        reviews = relationship("Review", backref="place",
                               cascade="all, delete-orphan")

        amenities = relationship("Amenity", secondary=place_amenity,
                                 back_populates="place_amenities",
                                 viewonly=False)
    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """
            get list of Review instances with
            place_id equals to the current Place.id
            """
            list_reviews = []
            all_reviews = models.storage.all(Review)
            for review in all_reviews:
                if review.place_id == Place.id:
                    list_reviews.append(review)
            return list_reviews

        @property
        def amenities(self):
            """
            returns the list of Amenity instances based on the attribute
            amenity_ids that contains all Amenity.id linked to the Place
            """
            amenity_objs = []
            amenity = models.storage.all(models.amenity.Amenity)
            for amenity_value in amenity.values():
                if amenity_value.id in self.amenity_ids:
                    amenity_objs.append(amenity_value)
            return amenity_objs

        @amenities.setter
        def amenities(self, obj):
            """
            adds an Amenity.id to the attribute amenity_ids if obj is
            an instance of Amenity
            """
            if isinstance(obj, models.amenity.Amenity):
                self.amenity_ids.append(obj.id)

    def __init__(self, *args, **kwargs):
        """Initialize Place instance."""
        super().__init__(*args, **kwargs)
