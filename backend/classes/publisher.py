from backend.classes.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Publisher(Base):
    __tablename__ = 'publishers'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    items = relationship('DBItem', backref='publisher_items')
