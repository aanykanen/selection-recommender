import json
import os
import pickle
import sys

import numpy as np

from sklearn import metrics
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

sys.path.append('..')
from backend.api.api_utils import get_recommendation
from backend.ml.metric_utils import save_confusion_matrix
from backend.ml.ml_utils import load_data_classification
from backend.ml.ml_conf import PREPROCESS_FILE_PATH
from backend.classes.subject import Subject
from backend.classes.serie import Series
from backend.classes.publisher import Publisher
from backend.classes.genre import Genre
from backend.classes.biblio import Biblio
from backend.classes.author import Author

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras.preprocessing.text import Tokenizer


# Make Keras eat less GPU memory if using GPU
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

def get_req(item, session):
    """
    Parses http-request like information from Item object

    :param item: Item-object to parse request-like dict from
    :param session: database session
    """
    req = {}

    if len(item.authors) > 0:
        db_author = session.query(Author).filter(
            Author.name == item.authors[0]).first()
        if db_author == None:
            req['author'] = item.authors[0].replace(' ', '_')
        else:
            req['author'] = db_author.id

    if len(item.publishers) > 0:
        db_publisher = session.query(Publisher).filter(
            Publisher.name == item.publishers[0]).first()
        if db_publisher == None:
            req['publisher'] = item.publishers[0].replace(' ', '_')
        else:
            req['publisher'] = db_publisher.id

    if len(item.series) > 0:
        db_series = session.query(Series).filter(
            Series.label == item.series[0]).first()
        if db_series == None:
            req['series'] = item.series[0].replace(' ', '_')
        else:
            req['series'] = db_series.id

    if len(item.genres) > 0:
        genres = []
        for g in item.genres:
            db_genre = session.query(Genre).filter(Genre.label == g).first()
            if db_genre == None:
                genres.append(str(g).replace(' ', '_'))
            else:
                genres.append(str(db_genre.id))
        req['genres'] = ' '.join(genres)

    if len(item.subjects) > 0:
        subjects = []
        for s in item.subjects:
            db_subject = session.query(Subject).filter(
                Subject.label == s).first()
            if db_subject == None:
                subjects.append(str(s).replace(' ', '_'))
            else:
                subjects.append(str(db_subject.id))
        req['subjects'] = ' '.join(subjects)

    return req


def recommend(i, session, tokenizer, classifier, field_lengths):
    """
    Makes the prediction/recommendation using the overall recommender system.

    :param i: item that recommendation is based on
    :param session: database session
    :param tokenizer: tokenizer for tokenizing features
    :param classifier: classifier to be used for ML prediction
    """
    recommendation = get_recommendation(i, session, tokenizer, classifier, field_lengths)
    final_score = recommendation['recommendation_score']

    if final_score > 1:
        return (1, recommendation)
    elif final_score < 0:
        return (-1, recommendation)
    else:
        return (0, recommendation)


if __name__ == "__main__":
    """
    This script tests the overall recommender system accuracy.
    """
    engine = create_engine(f'sqlite:///data/recommender.db', echo=False)
    Session = sessionmaker(bind=engine)
    session = Session()

    X_test, y_test = load_data_classification(
        PREPROCESS_FILE_PATH['testing'], full_rs=True)


    print(f'Test set has {len(y_test)} items.\n')

    class_distribution = np.unique(y_test, return_counts=True)
    num_classes = len(class_distribution[0])
    print('\nData class distribution is following in test set:')
    for class_, count in zip(class_distribution[0], class_distribution[1]):
        print(f'  class {class_}: {count} items')

    X_test = [get_req(x, session) for x in X_test]
    results = []

    y_rec = []

    for i, sample in enumerate(X_test):
        recommendation = recommend(sample, session, TOKENIZERS, MODEL, FIELD_LENGTHS)
        y_rec.append(recommendation[0])

        r = recommendation[1]
        r['true_class'] = int(y_test[i])
        results.append(r)

    y_rec = np.array(y_rec)
    accuracy = metrics.accuracy_score(y_test, y_rec)
    cm = metrics.confusion_matrix(y_test, y_rec)

    print(f'Final accuracy: {round(accuracy, 2) * 100}%')
    print(f'Confusion matrix: {cm}')

    with open('metrics/rs_test_log.txt', 'a') as f:
        f.write(f'Accuracy: {round(accuracy, 2) * 100} %\n')

    pickle.dump(cm, open('metrics/final_rs_cm.pkl', 'wb'))

    with open('metrics/rs_results.json', 'w') as f:
        json.dump(results, f)
