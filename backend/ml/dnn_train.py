import copy
import os
import pickle
import sys
import time

import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow.keras.optimizers import *
from tensorflow.keras import layers, Model
from tensorflow.keras.preprocessing.text import Tokenizer
from sklearn.model_selection import train_test_split
from sklearn import metrics

from ml_conf import *
from ml_utils import *
from ml_models import *

TERMINAL_SIZE = os.get_terminal_size()[0]

if __name__ == "__main__":
    """
    This script trains dnn model using entity embeddings. Run only if wish to run
    comparison between models.
    """
    print('\n' + '*' * TERMINAL_SIZE)
    print('ML MODEL TRAINING STARTS')

    if not os.path.exists('models'):
        os.makedirs('models')

    X_train, y_train = load_data_classification(PREPROCESS_FILE_PATH['training'], augment=True)
    X_valid, y_valid = load_data_classification(PREPROCESS_FILE_PATH['validating'], augment=True)
    X_test, y_test = load_data_classification(PREPROCESS_FILE_PATH['testing'])

    X_train = X_train + X_valid
    y_train = np.array(y_train.tolist() + y_valid.tolist())

    assert len(X_train) == len(y_train)
    print(f'\nTraining set has {len(y_train)} items')
    print(f'Testing set has {len(y_test)} items')

    class_distribution = np.unique(y_train, return_counts=True)
    num_classes = len(class_distribution[0])
    print('\nClass distribution is following in training set:')
    for class_, count in zip(class_distribution[0], class_distribution[1]):
        print(f'  class {class_}: {count} items')

    class_distribution = np.unique(y_test, return_counts=True)
    num_classes = len(class_distribution[0])
    print('\nClass distribution is following in test set:')
    for class_, count in zip(class_distribution[0], class_distribution[1]):
        print(f'  class {class_}: {count} items')

    # Authors
    author_tokenizer_train = list(
        set([x.get_feature('authors') for x in X_train]))
    author_tokenizer = Tokenizer(lower=False, split='#', filters='')
    author_tokenizer.fit_on_texts(author_tokenizer_train)
    author_vocab_size = len(author_tokenizer.word_index)
    reverse_author_map = dict(
        map(reversed, author_tokenizer.word_index.items()))
    pickle.dump(author_tokenizer, open('models/author_tokenizer.pkl', 'wb'))
    print(f'\nThere are {author_vocab_size} distinct authors')

    # Series
    series_tokenizer_train = list(
        set([x.get_feature('series') for x in X_train]))
    series_tokenizer = Tokenizer(lower=False, split='#', filters='')
    series_tokenizer.fit_on_texts(series_tokenizer_train)
    series_vocab_size = len(series_tokenizer.word_index)
    reverse_series_map = dict(
        map(reversed, series_tokenizer.word_index.items()))
    pickle.dump(series_tokenizer, open('models/series_tokenizer.pkl', 'wb'))
    print(f'There are {series_vocab_size} distinct series')

    # Subjects
    subjects_tokenizer_train = list(
        set([x.get_feature('subjects') for x in X_train]))
    subjects_tokenizer = Tokenizer(lower=False, split='#', filters='')
    subjects_tokenizer.fit_on_texts(subjects_tokenizer_train)
    subjects_vocab_size = len(subjects_tokenizer.word_index)
    reverse_subject_map = dict(
        map(reversed, subjects_tokenizer.word_index.items()))
    pickle.dump(subjects_tokenizer, open(
        'models/subjects_tokenizer.pkl', 'wb'))
    print(f'There are {subjects_vocab_size} distinct subjects')

    # Genres
    genres_tokenizer_train = list(
        set([x.get_feature('genres') for x in X_train]))
    genres_tokenizer = Tokenizer(lower=False, split='#', filters='')
    genres_tokenizer.fit_on_texts(genres_tokenizer_train)
    genres_vocab_size = len(genres_tokenizer.word_index)
    reverse_genres_map = dict(
        map(reversed, genres_tokenizer.word_index.items()))
    pickle.dump(genres_tokenizer, open('models/genres_tokenizer.pkl', 'wb'))
    print(f'There are {genres_vocab_size} distinct genres')

    # Publishers
    publishers_tokenizer_train = list(
        set([x.get_feature('publishers') for x in X_train]))
    publishers_tokenizer = Tokenizer(lower=False, split='#', filters='')
    publishers_tokenizer.fit_on_texts(publishers_tokenizer_train)
    publishers_vocab_size = len(publishers_tokenizer.word_index)
    reverse_publishers_map = dict(
        map(reversed, publishers_tokenizer.word_index.items()))
    pickle.dump(publishers_tokenizer, open(
        'models/publishers_tokenizer.pkl', 'wb'))
    print(f'There are {publishers_vocab_size} distinct publishers\n')

    authors_max_len = max([len(x.authors) for x in X_train])
    genres_max_len = max([len(x.genres) for x in X_train])
    series_max_len = max([len(x.series) for x in X_train])
    subjects_max_len = max([len(x.subjects) for x in X_train])
    publishers_max_len = max([len(x.publishers) for x in X_train])

    field_lengths = {
        'authors': authors_max_len,
        'genres': genres_max_len,
        'publishers': publishers_max_len,
        'series': series_max_len,
        'subjects': subjects_max_len
    }
    pickle.dump(field_lengths, open('models/field_lengths.pkl', 'wb'))

    def prepare_data(X):
        X1, X2, X3, X4, X5 = [[] for x in range(5)]

        # Update item features to encoded versions, pad in same iteration
        for item in X:
            data_authors = author_tokenizer.texts_to_sequences([item.get_feature('authors')])[0]
            data_authors = pad_sequence(data_authors, authors_max_len)
            X1.append(data_authors)

            data_genres = genres_tokenizer.texts_to_sequences([item.get_feature('genres')])[0]
            data_genres = pad_sequence(data_genres, genres_max_len)
            X2.append(data_genres)

            data_series = series_tokenizer.texts_to_sequences([item.get_feature('series')])[0]
            data_series = pad_sequence(data_series, series_max_len)
            X3.append(data_series)

            data_subjects = subjects_tokenizer.texts_to_sequences([item.get_feature('subjects')])[0]
            data_subjects = pad_sequence(data_subjects, subjects_max_len)
            X4.append(data_subjects)

            data_publishers = publishers_tokenizer.texts_to_sequences([item.get_feature('publishers')])[0]
            data_publishers = pad_sequence(data_publishers, publishers_max_len)
            X5.append(data_publishers)

        return [np.array(X1), np.array(X2), np.array(X3), np.array(X4), np.array(X5)]

    X_train = prepare_data(X_train)
    X_test = prepare_data(X_test)

    model = build_ee_dnn(
        authors_max_len,
        author_vocab_size,
        genres_max_len,
        genres_vocab_size,
        series_max_len,
        series_vocab_size,
        subjects_max_len,
        subjects_vocab_size,
        publishers_max_len,
        publishers_vocab_size,
        num_classes)

    optimizer = Nadam(learning_rate=0.000001)
    model.compile(loss='sparse_categorical_crossentropy',
                  optimizer=optimizer, metrics=['accuracy'])

    print('\n' + '*' * TERMINAL_SIZE)
    print('TRAINING WITH TRAINING SET')
    history = model.fit(X_train, y_train, epochs=EPOCHS, verbose=1, batch_size=8)

    print('\n' + '*' * TERMINAL_SIZE)
    print('VALIDATING MODEL WITH VALIDATION SET')
    loss = model.evaluate(X_test, y_test)

    model.save('models/dnn')
    print('\nDNN MODEL HAS BEEN TRAINED AND SAVED\n')
