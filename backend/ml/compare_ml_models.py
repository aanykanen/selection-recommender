import os
import sys
import pickle

import lightgbm as lgb
import numpy as np

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from xgboost import XGBClassifier
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow import keras
from sklearn.feature_selection import SelectKBest, mutual_info_classif
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import LinearSVC
from sklearn.tree import DecisionTreeClassifier

from ml_utils import convert_features, load_data_classification, pad_sequence
from ml_conf import PREPROCESS_FILE_PATH
from metric_utils import features_to_text, test_model


TERMINAL_SIZE = os.get_terminal_size()[0]

if __name__ == "__main__":
    """
    This script compares different ML models. 
    Build DNN model before running the script.
    """

    if not os.path.exists('metrics'):
        os.makedirs('metrics')

    X_train, y_train = load_data_classification(
        PREPROCESS_FILE_PATH['training'], augment=True)
    X_valid, y_valid = load_data_classification(
        PREPROCESS_FILE_PATH['validating'], augment=True)
    X_test, y_test = load_data_classification(
        PREPROCESS_FILE_PATH['testing'])

    X_train = X_train + X_valid
    y_train = np.array(y_train.tolist() + y_valid.tolist())

    print(f'\nTraining set has {len(y_train)} items')
    print(f'Test set has {len(y_test)} items')

    # Class distributions
    class_distribution = np.unique(y_train, return_counts=True)
    num_classes = len(class_distribution[0])
    print('\nData class distribution is following in training set:')

    for class_, count in zip(class_distribution[0], class_distribution[1]):
        print(f'  class {class_}: {count} items')

    class_distribution = np.unique(y_test, return_counts=True)
    num_classes = len(class_distribution[0])
    print('\nClass distribution is following in test set:')
    for class_, count in zip(class_distribution[0], class_distribution[1]):
        print(f'  class {class_}: {count} items')

    # Feature vocab for non DNN algorithms
    train_feature_vocab = [x.get_feature_string() for x in X_train]

    # Preprocess: tokenize features
    t = Tokenizer(lower=False, split='#',
                  filters='!"$%&()*+./:;<=>?@[\\]^`{|}~\n')
    t.fit_on_texts(train_feature_vocab)
    feature_vocab_size = len(t.word_index)
    print(f'\nThere are total of {len(t.word_index)} different features')

    # Encode features for training set and test set
    X_train_onehot = [convert_features(x, t) for x in X_train]
    X_test_onehot = [convert_features(x, t) for x in X_test]

    # Allows transforming from indexes back to features
    reverse_word_map = dict(map(reversed, t.word_index.items()))

    # COMPARISON OF DIFFERENT MODELS STARTS
    #
    # LIST OF MODELS COMPARED:
    # - Decision Tree classifier
    # - Deep neural network trained using entity embeddings
    # - Random Forest
    # - Support Vector Classification (SVC)
    # - XGBoost
    # - LightGBM

    with open('metrics/accuracies.csv', 'w') as f:
        pass

    # Loading DNN model
    authors_tokenizer = pickle.load(open('models/author_tokenizer.pkl', 'rb'))
    publishers_tokenizer = pickle.load(
        open('models/publishers_tokenizer.pkl', 'rb'))
    series_tokenizer = pickle.load(open('models/series_tokenizer.pkl', 'rb'))
    genres_tokenizer = pickle.load(open('models/genres_tokenizer.pkl', 'rb'))
    subjects_tokenizer = pickle.load(
        open('models/subjects_tokenizer.pkl', 'rb'))
    field_lengths = pickle.load(open('models/field_lengths.pkl', 'rb'))
    dnn_model = keras.models.load_model('models/dnn')

    X1_test, X2_test, X3_test, X4_test, X5_test = [[] for x in range(5)]

    for i in X_test:
        author = authors_tokenizer.texts_to_sequences(
            [i.get_feature('authors')])[0]
        author = pad_sequence(author, field_lengths['authors'])
        X1_test.append(author)

        genres = genres_tokenizer.texts_to_sequences(
            [i.get_feature('genres')])[0]
        genres = pad_sequence(genres, field_lengths['genres'])
        X2_test.append(genres)

        series = series_tokenizer.texts_to_sequences(
            [i.get_feature('series')])[0]
        series = pad_sequence(series, field_lengths['series'])
        X3_test.append(series)

        subject = subjects_tokenizer.texts_to_sequences(
            [i.get_feature('subjects')])[0]
        subject = pad_sequence(subject, field_lengths['subjects'])
        X4_test.append(subject)

        publisher = publishers_tokenizer.texts_to_sequences(
            [i.get_feature('publishers')])[0]
        publisher = pad_sequence(publisher, field_lengths['publishers'])
        X5_test.append(publisher)

    X1_test = np.array(X1_test)
    X2_test = np.array(X2_test)
    X3_test = np.array(X3_test)
    X4_test = np.array(X4_test)
    X5_test = np.array(X5_test)

    print('\n' + '*' * TERMINAL_SIZE)
    print('Testing DNN')

    test_model(dnn_model, [X1_test, X2_test, X3_test,
                           X4_test, X5_test], y_test, 'DNN ENTITY EMBEDDINGS')

    def test_non_dnn_models(X_train_onehot, y_train, X_test_onehot, y_test, all_features=True):
        """Builds and tests all non dnn models included into comparison"""
        # Decision tree
        print('\n' + '*' * TERMINAL_SIZE)
        print('Testing Decision Tree')

        dt_classifier = DecisionTreeClassifier()
        dt_classifier.fit(X_train_onehot, y_train)
        dt_classifier_name = 'DECISION TREE' if all_features else 'DECISION TREE SF'
        test_model(dt_classifier, X_test_onehot, y_test, dt_classifier_name)

        # Random forest
        print('\n' + '*' * TERMINAL_SIZE)
        print('Testing Random Forest')
        rf_classifier = RandomForestClassifier()
        rf_classifier.fit(X_train_onehot, y_train)
        rf_classifier_name = 'RANDOM FOREST' if all_features else 'RANDOM FOREST SF'
        test_model(rf_classifier, X_test_onehot, y_test, rf_classifier_name)

        # Linear SVC
        print('\n' + '*' * TERMINAL_SIZE)
        print('Testing Linear SVC')
        svc_classifier = LinearSVC()
        svc_classifier.fit(X_train_onehot, y_train)
        svc_classifier_name = 'LINEAR SVC' if all_features else 'LINEAR SVC SF'
        test_model(svc_classifier, X_test_onehot, y_test, svc_classifier_name)

        # XGBoost
        print('\n' + '*' * TERMINAL_SIZE)
        print('Testing XGBoost')
        xgboost = XGBClassifier()
        xgboost.max_depth = 9
        xgboost.max_leaves = 63

        eval_set = [(np.array(X_test_onehot), y_test)]
        xgboost.fit(np.array(X_train_onehot), y_train, early_stopping_rounds=10,
                    eval_set=eval_set, eval_metric='error', verbose=False)
        xgboost_name = 'XGBOOST' if all_features else 'XGBOOST SF'
        test_model(xgboost, np.array(X_test_onehot), y_test, xgboost_name)

        # LightGBM
        lgb_name = 'LIGHTGBM' if all_features else 'LIGHTGBM SF'
        lgb_train = lgb.Dataset(np.array(X_train_onehot), label=y_train)
        lgb_test = lgb.Dataset(np.array(X_test_onehot), label=y_test)

        # Params for LightGBM
        print('\n' + '*' * TERMINAL_SIZE)
        print('Testing LightGBM')

        params = {}
        params['objective'] = 'binary'
        params['metric'] = 'binary_logloss'
        params['max_depth'] = 9,
        params['num_leaves'] = 63
        params['verbose'] = -1

        lgb_classifier = lgb.train(params, lgb_train, valid_sets=[
                                   lgb_train, lgb_test], early_stopping_rounds=5, verbose_eval=False)
        test_model(lgb_classifier, np.array(X_test_onehot), y_test, lgb_name)

    test_non_dnn_models(X_train_onehot, y_train, X_test_onehot, y_test)

    print('\n' + '*' * TERMINAL_SIZE)
    print('Selecting best features for next comparison, this might take a while')

    # Feature selection: reducing features to top 1000 features
    fs = SelectKBest(score_func=mutual_info_classif, k=1000)
    fs.fit(X_train_onehot, y_train)
    X_train_fs = fs.transform(X_train_onehot)
    X_test_fs = fs.transform(X_test_onehot)

    # Test all non dnn models with reduced amount of features
    test_non_dnn_models(X_train_fs, y_train, X_test_fs,
                        y_test, all_features=False)
