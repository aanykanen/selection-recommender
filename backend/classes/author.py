from backend.classes.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Author(Base):
    __tablename__ = 'authors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    items = relationship('DBItem', backref='author_items')
