import copy
import pickle
import random
import sys

import numpy as np

sys.path.append('..')
from backend.classes.item import Item
from backend.ml.ml_conf import *


def load_data_classification(filepath, augment=False, full_rs=False):
    """
    Loads data and processes it so that the label is one of two classes defined. 
    Breakpoint for circulation is defined in conf.py (default: 4 loans in first 12 months).

    :param filepath: path to file which has serialized members of Item class
    :param augment: determines if class 0 members should be augmented in case classes are imbalanced
    :param full_rs: changes label from class 0 to -1. Use if evaluating full rs using api/test_recommender.py
    """

    tmp_items = []
    tmp_bib_ids = []

    items = pickle.load(open(filepath, 'rb'))

    print(f'ITEM COUNT: {len(items)}')

    for i in items:
        if i.get_feature_count() < MIN_FEATURES:
            continue

        sequence = i.circulation_sequence
        if len(sequence) < MONTHS_TO_AVG:
            continue

        tmp_x = {'info': i, 'label': 0}
        start_avg_circulation = np.mean(sequence[:MONTHS_TO_AVG])

        # Labeling, uses breakpoint defined in conf
        if start_avg_circulation >= CIRCULATION_CLASSIFICATION_BREAKPOINT:
            tmp_x['label'] = 1

        if full_rs and tmp_x['label'] == 0:
            tmp_x['label'] = -1

        # Design decision: for same bib, using the best label available through items
        if i.bib_id in tmp_bib_ids:
            bib_idx = tmp_bib_ids.index(i.bib_id)
            if tmp_items[bib_idx]['label'] < tmp_x['label']:
                tmp_items[bib_idx]['label'] = tmp_x['label']
            if tmp_items[bib_idx]['info'].get_feature_count() < i.get_feature_count():
                tmp_items[bib_idx]['info'] = i
        else:
            tmp_items.append(tmp_x)
            tmp_bib_ids.append(tmp_x['info'].bib_id)

    X, y = [], []
    n_augmented = 0

    print(f'ACCEPTED ITEMS: {len(tmp_items)}')

    for i in tmp_items:
        if augment and i['label'] == 0:
            if i['info'].get_feature_count() > 10:
                augmented_items = augment_item(i, 3)
                for ai in augmented_items:
                    n_augmented += 1
                    X.append(ai['info'])
                    y.append(ai['label'])

                # The original item is not calculated as augmented
                n_augmented -= 1
            else:
                X.append(i['info'])
                y.append(i['label'])
        else:
            X.append(i['info'])
            y.append(i['label'])

    print(f'Augmented {n_augmented} items for class 0')
    print(f'ITEMS TOTAL: {len(X)}')

    return X, np.array(y)


def convert_features(x, tokenizer):
    """
    Converts features to one one-hot vectors using tokenizer.

    :param x: sample belonging into the Item class
    :param tokenizer: tokenizer used for feature transformation
    """
    return tokenizer.texts_to_matrix([x.get_feature_string()])[0]


def pad_sequence(sequence, maxlen):
    """
    Pads sequence with zeros until its length is equal to max length.

    :param sequence: sequence to be padded in array form
    :param maxlen: length sequence will be padded to
    """
    if len(sequence) > maxlen:
        sequence = sequence[:maxlen]

    while len(sequence) < maxlen:
        sequence.append(0)

    return sequence


def augment_item(item, max_augment):
    """
    Creates new versions of item by deleting appropriate features one at a time.

    :param item: item to be augmented
    :param max_augment: maximum number of augmented items to return
    """
    augmented_items = []

    orig_item = item['info']
    feature_counts = orig_item.get_feature_counts()
    features_to_augment = dict(
        filter(lambda x: x[1] > 3, feature_counts.items()))

    for f in features_to_augment.keys():
        for i in range(len(orig_item[f])):
            new_item = copy.deepcopy(orig_item)
            feature_to_delete = new_item[f][i]
            new_item[f].remove(feature_to_delete)
            augmented_items.append({'info': new_item, 'label': item['label']})

    assert id(item['info']) != id(augmented_items[0]['info'])

    if len(augmented_items) > max_augment:
        augmented_sample = random.sample(augmented_items, max_augment)
    else:
        augmented_sample = augmented_items

    augmented_sample.append(item)
    return augmented_sample
