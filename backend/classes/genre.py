from backend.classes.base import Base
from backend.classes.db_item import item_genre
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Genre(Base):
    __tablename__ = 'genres'

    id = Column(Integer, primary_key=True)
    label = Column(String)
    items = relationship('DBItem', item_genre)
