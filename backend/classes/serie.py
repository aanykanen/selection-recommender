from backend.classes.base import Base
from backend.classes.db_item import item_serie
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Series(Base):
    __tablename__ = 'series'

    id = Column(Integer, primary_key=True)
    label = Column(String)
    items = relationship('DBItem', item_serie)
