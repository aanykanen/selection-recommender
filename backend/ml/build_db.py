import pickle
import sys

from sqlalchemy import create_engine
from sqlalchemy.orm import relationship, backref, sessionmaker

sys.path.append('..')

from backend.ml.ml_conf import PREPROCESS_FILE_PATH
from backend.classes.subject import Subject
from backend.classes.serie import Series
from backend.classes.publisher import Publisher
from backend.classes.genre import Genre
from backend.classes.db_item import DBItem
from backend.classes.biblio import Biblio
from backend.classes.base import Base
from backend.classes.author import Author


def save_item(item, session):
    """
    Saves an item to database.

    :param item: Item-class object to save to database
    :param session: database session
    """

    # Sanity check if item already in db
    db_item = session.query(DBItem).filter(DBItem.id == item.item_id).first()

    if db_item:
        return

    db_item = DBItem(
        id=item.item_id,
        acquired=item.acquired,
        title=item.title,
        pub_year=item.pubyear,
        deleted=item.deleted,
        circulation_sequence=item.circulation_sequence,
        last_borrowed=item.last_borrowed)
    session.add(db_item)

    # Process bib
    db_bib = session.query(Biblio).filter(Biblio.id == item.bib_id).first()
    if not db_bib:
        db_bib = Biblio(id=item.bib_id, title=item.title)
        session.add(db_bib)
        session.flush()

    db_bib.items.append(db_item)

    # Process author
    if len(item.authors) > 0:
        db_author = session.query(Author).filter(
            Author.name == item.authors[0]).first()
        if not db_author:
            db_author = Author(name=item.authors[0])
            session.add(db_author)
            session.flush()

        db_author.items.append(db_item)

    # Process publisher
    if len(item.publishers) > 0:
        db_publisher = session.query(Publisher).filter(
            Publisher.name == item.publishers[0]).first()
        if not db_publisher:
            db_publisher = Publisher(name=item.publishers[0])
            session.add(db_publisher)
            session.flush()
        db_publisher.items.append(db_item)

    # Process genre
    for genre in item.genres:
        db_genre = session.query(Genre).filter(Genre.label == genre).first()
        if not db_genre:
            db_genre = Genre(label=genre)
            session.add(db_genre)
            session.flush()

        db_genre.items.append(db_item)

    # Process series
    for serie in item.series:
        db_series = session.query(Series).filter(Series.label == serie).first()
        if not db_series:
            db_series = Series(label=serie)
            session.add(db_series)
            session.flush()

        db_series.items.append(db_item)

    # Process subject terms
    for subject in item.subjects:
        db_subject = session.query(Subject).filter(
            Subject.label == subject).first()
        if not db_subject:
            db_subject = Subject(label=subject)
            session.add(db_subject)
            session.flush()

        db_subject.items.append(db_item)

    session.commit()
    return True


if __name__ == "__main__":
    """
    This script builds database for the recommender system.
    Takes ~6-7h with 50k records. 
    """
    engine = create_engine(f'sqlite:///data/recommender.db', echo=False)

    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine, checkfirst=True)

    Session = sessionmaker(bind=engine)
    session = Session()

    items = pickle.load(open(PREPROCESS_FILE_PATH['db_constructing'], 'rb'))

    for item in items:
        save_item(item, session)

    session.close()
