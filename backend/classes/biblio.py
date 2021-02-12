from backend.classes.base import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship


class Biblio(Base):
    __tablename__ = 'biblio'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    items = relationship('DBItem', backref='biblio_items')
