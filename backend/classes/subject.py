from backend.classes.base import Base
from backend.classes.db_item import item_subject

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Subject(Base):
    __tablename__ = 'subjects'

    id = Column(Integer, primary_key=True)
    label = Column(String)
    items = relationship('DBItem', item_subject)
