from backend.classes.base import Base
from sqlalchemy import Column, Date, ForeignKey, Integer, PickleType, String, Table, Text
from sqlalchemy.orm import relationship

# Association tables
item_subject = Table('ItemSubject', Base.metadata,
                     Column('item_id', Integer, ForeignKey('items.id')),
                     Column('subject_id', Integer, ForeignKey('subjects.id')))
item_genre = Table('ItemGenre', Base.metadata,
                   Column('item_id', Integer, ForeignKey('items.id')),
                   Column('genre_id', Integer, ForeignKey('genres.id')))
item_serie = Table('ItemSerie', Base.metadata,
                   Column('item_id', Integer, ForeignKey('items.id')),
                   Column('serie_id', Integer, ForeignKey('series.id')))


class DBItem(Base):
    __tablename__ = 'items'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    pub_year = Column(Integer)
    acquired = Column(Date)
    last_borrowed = Column(Date)
    circulation_sequence = Column(PickleType)
    deleted = Column(Date)
    author = relationship('Author')
    author_id = Column(Integer, ForeignKey('authors.id'))
    bib = relationship('Biblio')
    bib_id = Column(Integer, ForeignKey('biblio.id'))
    genre = relationship('Genre', secondary=item_genre)
    publisher = relationship('Publisher')
    publisher_id = Column(Integer, ForeignKey('publishers.id'))
    subjects = relationship('Subject', secondary=item_subject)
    series = relationship('Series', secondary=item_serie)

    def __repr__(self):
        return f'<Book(title={self.title}, subjects={self.subjects}, genres={self.genre}, acquired={self.acquired}>'
