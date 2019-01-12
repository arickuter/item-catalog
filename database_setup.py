import os
import sys
import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Text
from sqlalchemy import DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


class Categories(Base):
    """Create Categories table."""
    __tablename__ = 'categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    @property
    def serialize(self):
        """Format to serialize category in."""

        return {
            'id': self.id,
            'name': self.name,
        }


class Items(Base):
    """Create Items table."""
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    title = Column(String(250), nullable=False)
    description = Column(String(250), nullable=False)
    creator_email = Column(String(250), nullable=False)
    cat_id = Column(Integer, ForeignKey('categories.id'))
    categories = relationship(Categories)

    @property
    def serialize(self):
        """Format to serialize item in."""

        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'email': self.creator_email,
            'cat_id': self.cat_id,
        }


engine = create_engine('sqlite:///catalog.db')
Base.metadata.create_all(engine)
