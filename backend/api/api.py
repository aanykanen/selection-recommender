import numpy as np
import math
import os
import pickle
import sys

from flask import abort, jsonify
from flask import Flask
from flask_cors import CORS
from flask_restful import Api, Resource, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy_session import flask_scoped_session

from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

sys.path.append('..')
from backend.api.api_utils import *
from backend.classes.item import Item
from backend.classes.schemas import *
from recommender_conf import *

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer


# Make Keras reserve less GPU memory if using GPU
gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
  try:
    for gpu in gpus:
      tf.config.experimental.set_memory_growth(gpu, True)
  except RuntimeError as e:
    print(e)

# DNN setup
AUTHORS_TOKENIZER = pickle.load(open('models/author_tokenizer.pkl', 'rb'))
PUBLISHERS_TOKENIZER = pickle.load(open('models/publishers_tokenizer.pkl', 'rb'))
SERIESS_TOKENIZER = pickle.load(open('models/series_tokenizer.pkl', 'rb'))
GENRES_TOKENIZER = pickle.load(open('models/genres_tokenizer.pkl', 'rb'))
SUBJECTS_TOKENIZER = pickle.load(open('models/subjects_tokenizer.pkl', 'rb'))
FIELD_LENGTHS = pickle.load(open('models/field_lengths.pkl', 'rb'))
MODEL = keras.models.load_model('models/dnn')
TOKENIZERS = {
    'author': AUTHORS_TOKENIZER,
    'publisher': PUBLISHERS_TOKENIZER,
    'series': SERIESS_TOKENIZER,
    'genres': GENRES_TOKENIZER,
    'subjects': SUBJECTS_TOKENIZER
}
keras.backend.clear_session()

# App config
app = Flask(__name__)
CORS(app, resources={r'/api/*': {'origins': '*'}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data/recommender.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
ma = Marshmallow(app)
api = Api(app)

# Database init
engine = create_engine(f'sqlite:///data/recommender.db', echo=False)
session_factory = sessionmaker(bind=engine)
session = flask_scoped_session(session_factory, app)


@app.errorhandler(404)
def not_found(e):
    return jsonify(error=str(e)), 404


class AuthorListResource(Resource):
    def get(self):
        authors = session.query(Author).all()
        if authors is None:
            abort(404, description='Author not found')
        else:
            return authors_schema.dump(authors)


class AuthorResource(Resource):
    def get(self, author_id):
        author = session.query(Author).filter(Author.id == author_id).first()
        if author is None:
            abort(404, description='Author not found')
        else:
            return author_schema.dump(author)


class BiblioListResource(Resource):
    def get(self):
        biblio = session.query(Biblio).all()
        if biblio is None:
            abort(404, description='Biblio not found')
        else:
            return biblios_schema.dump(biblio)


class BiblioResource(Resource):
    def get(self, biblio_id):
        biblio = session.query(Biblio).filter(Biblio.id == biblio_id).first()
        if biblio is None:
            abort(404, description='Biblio not found')
        else:
            return biblio_schema.dump(biblio)


class GenreResource(Resource):
    def get(self, genre_id):
        genre = session.query(Genre).filter(Genre.id == genre_id).first()
        if genre is None:
            abort(404, description='Genre not found')
        else:
            return genre_schema.dump(genre)


class GenreListResource(Resource):
    def get(self):
        genres = session.query(Genre).all()
        if genres is None:
            abort(404, description='Genre not found')
        else:
            return genres_schema.dump(genres)


class ItemResource(Resource):
    def get(self, item_id):
        item = session.query(DBItem).filter(DBItem.id == item_id).first()
        if item is None:
            abort(404, description='Item not found')
        else:
            item_from_schema = item_schema.dump(item)
            item_from_schema['circulation_sequence'] = item.circulation_sequence
            item_from_schema['series'] = item_from_schema['series'][0] if len(
                item_from_schema['series']) > 0 else None

            # Hack until DB is fixed
            item_from_schema['genres'] = item_from_schema['genre']
            return jsonify(item_from_schema)


class PublisherResource(Resource):
    def get(self, publisher_id):
        publisher = session.query(Publisher).filter(
            Publisher.id == publisher_id).first()
        if publisher is None:
            abort(404, description='Publisher not found')
        else:
            return publisher_schema.dump(publisher)


class PublishersResource(Resource):
    def get(self):
        publishers = session.query(Publisher).all()
        if publishers is None:
            abort(404, description='Publishers not found')
        else:
            return publishers_schema.dump(publishers)


class SeriesListResource(Resource):
    def get(self):
        series = session.query(Series).all()
        if series is None:
            abort(404, description='Series not found')
        else:
            return series_m_schema.dump(series)


class SeriesResource(Resource):
    def get(self, series_id):
        series = session.query(Series).filter(Series.id == series_id).first()
        if series is None:
            abort(404, description='Series not found')
        else:
            return series_schema.dump(series)


class SubjectListResource(Resource):
    def get(self):
        subjects = session.query(Subject).all()
        if subjects is None:
            abort(404, description='Subjects not found')
        else:
            return subjects_schema.dump(subjects)


class SubjectResource(Resource):
    def get(self, subject_id):
        subject = session.query(Subject).filter(
            Subject.id == subject_id).first()
        if subject is None:
            abort(404, description='Subject not found')
        else:
            return subject_schema.dump(subject)


class SelectionRecommendationResource(Resource):
    def get(self):
        args = request.args
        res = get_recommendation(args, session, TOKENIZERS, MODEL, FIELD_LENGTHS)

        return jsonify(res)


# Basic resources
api.add_resource(AuthorListResource, '/api/authors/')
api.add_resource(AuthorResource, '/api/authors/<int:author_id>')
api.add_resource(BiblioListResource, '/api/biblio/')
api.add_resource(BiblioResource, '/api/biblio/<int:biblio_id>')
api.add_resource(GenreListResource, '/api/genres/')
api.add_resource(GenreResource, '/api/genres/<int:genre_id>')
api.add_resource(ItemResource, '/api/items/<int:item_id>')
api.add_resource(PublishersResource, '/api/publishers/')
api.add_resource(PublisherResource, '/api/publishers/<int:publisher_id>')
api.add_resource(SeriesListResource, '/api/series/')
api.add_resource(SeriesResource, '/api/series/<int:series_id>')
api.add_resource(SubjectListResource, '/api/subjects/')
api.add_resource(SubjectResource, '/api/subjects/<int:subject_id>')

# Recommendation resource
api.add_resource(SelectionRecommendationResource,
                 '/api/recommendation/selection')

if __name__ == "__main__":
    app.run(debug=True, port=5000)
