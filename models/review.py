#!/usr/bin/python3
"""Review module"""
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship

storage_type = getenv("HBNB_TYPE_STORAGE")


class Review(BaseModel, Base):
    """Review (models/review.py):

    Purpose: Represents a review for a place.

    Attributes:
        place_id: string, optional - The ID of the place being reviewed.
        user_id: string, optional - The ID of the user who wrote the review.
        text: string, optional - The content of the review.

    Usage:
        Create a new instance of Review with
            optional parameters to represent different reviews."""

    __tablename__ = 'reviews'
    if storage_type == 'db':
        place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        text = Column(String(1024), nullable=False)
    else:
        place_id = ""
        user_id = ""
        text = ""

    def __init__(self, *args, **kwargs):
        """Initialize Place instance."""
        super().__init__(*args, **kwargs)
