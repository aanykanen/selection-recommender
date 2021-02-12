from backend.api.api import ma

from backend.classes.author import Author
from backend.classes.biblio import Biblio
from backend.classes.db_item import DBItem
from backend.classes.genre import Genre
from backend.classes.publisher import Publisher
from backend.classes.serie import Series
from backend.classes.subject import Subject


class AuthorSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Author

    id = ma.auto_field()
    name = ma.auto_field()
    items = ma.auto_field()


class BiblioSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Biblio

    id = ma.auto_field()
    title = ma.auto_field()
    items = ma.auto_field()


class GenreSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Genre

    id = ma.auto_field()
    label = ma.auto_field()
    items = ma.auto_field()


class ItemSchema(ma.SQLAlchemySchema):
    class Meta:
        model = DBItem

    id = ma.auto_field()
    title = ma.auto_field()
    pub_year = ma.auto_field()
    acquired = ma.auto_field()
    deleted = ma.auto_field()
    author = ma.auto_field()
    publisher = ma.auto_field()
    bib = ma.auto_field()
    genre = ma.auto_field()
    subjects = ma.auto_field()
    series = ma.auto_field()
    circulation_sequence = ma.auto_field()
    last_borrowed = ma.auto_field()


class PublisherSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Publisher

    id = ma.auto_field()
    name = ma.auto_field()
    items = ma.auto_field()


class SeriesSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Series

    id = ma.auto_field()
    label = ma.auto_field()
    items = ma.auto_field()


class SubjectSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Subject

    id = ma.auto_field()
    label = ma.auto_field()
    items = ma.auto_field()


author_schema = AuthorSchema()
authors_schema = AuthorSchema(many=True, only=('id', 'name'))

biblio_schema = BiblioSchema()
biblios_schema = BiblioSchema(many=True, only=('id', 'title'))

item_schema = ItemSchema()

genre_schema = GenreSchema()
genres_schema = GenreSchema(many=True, only=('id', 'label'))

publisher_schema = PublisherSchema()
publishers_schema = PublisherSchema(many=True, only=('id', 'name'))

series_schema = SeriesSchema()
series_m_schema = SeriesSchema(many=True, only=('id', 'label'))

subject_schema = SubjectSchema()
subjects_schema = SubjectSchema(many=True, only=('id', 'label'))
