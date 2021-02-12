import sys

import numpy as np

from sqlalchemy import func

sys.path.append('..')
from backend.classes.subject import Subject
from backend.classes.serie import Series
from backend.classes.publisher import Publisher
from backend.classes.item import Item
from backend.classes.genre import Genre
from backend.classes.db_item import DBItem
from backend.classes.biblio import Biblio
from backend.classes.base import Base
from backend.classes.author import Author
from backend.api.recommender_conf import *
from backend.ml.ml_utils import pad_sequence


def was_usable_feature(entity, tokenizer):
    """
    Returns true if tokenizer finds the entity and false if not.

    :param entity: entity in string form
    :param tokenizer: tokenizer used to transform entity into a feature vector form
    """
    return entity.replace(' ', '_') in tokenizer.word_index


def get_newitem_score(heading, t):
    """
    Returns score for new items. The score is different depending on
    the attribute type.

    :param heading: heading used for the entity
    :param t: type of the entity
    """
    ni_score = {
        'heading': heading,
        'new': True,
        'ml_feature': False
    }

    if t == 'Series':
        ni_score['score'] = {
            'stars': 3,
            'total_score': 0
        }
    elif t == 'Publisher':
        ni_score['score'] = {
            'stars': 1,
            'total_score': -2
        }
    elif t == 'Author':
        ni_score['score'] = {
            'stars': 4,
            'total_score': 1
        }
    else:
        ni_score['score'] = {
            'stars': 3,
            'total_score': 0
        }

    return ni_score


def get_trend(data, months=13, normalized=False):
    """
    Calculates trend given the circulation data.

    :param data: array consisting of circulation log data
    :param months: number of months to calculate the trend to
    :param normalized: boolean whether to normalize output based on item count
    """
    trend = [0 for x in range(months)]
    item_count = 0

    for sequence in data:
        for datapoint in range(min([len(sequence), months])):
            index = -datapoint - 1
            trend[index] += sequence[index]
            item_count += 1

    if normalized:
        if item_count > 0:
            trend = [x / item_count for x in trend]

    return trend[:12]


def calculate_totals(data, months=0):
    """
    Calculates total circulation given the data.

    :param data: circulation data
    :param months: how many latest months to include to calculations
    """
    result = {}
    for d in data:
        if d[0] not in result:
            if months <= 0:
                result[d[0]] = sum(d[1])
            else:
                result[d[0]] = sum(d[1][-months:])
        else:
            if months <= 0:
                result[d[0]] += sum(d[1])
            else:
                result[d[0]] += sum(d[1][-months:])

    result = list(result.items())
    result.sort(key=lambda x: x[1], reverse=True)
    return result


def calculate_normalized_totals(items, circulation):
    """
    Calculates normalized circulation.

    :param items: item data
    :param circulation: circulation data
    """
    items = dict(items)
    circulation = dict(circulation)
    result = {}

    for key in items.keys():
        result[key] = circulation[key] / items[key]

    result = list(result.items())
    result.sort(key=lambda x: x[1], reverse=True)
    return result


def rank_to_points(rank, total_items):
    """
    Calculates points from rank according to configurations.

    :param rank: rank of the item
    :param total_items: number of total items in same category
    """
    if rank <= int(total_items / 100 * TOP_RANK_PERCENTILE):
        return 1
    elif rank <= int(total_items / 100 * (100 - BOTTOM_RANK_PERCENTILE)):
        return 0
    else:
        return -1


def calculate_feature_score(itemcount_rank, normalized_circulation_rank, total_items):
    """
    Calculates score for a feature given the rank information.

    :param itemcount_rank: rank of item in item count category
    :param normalized_circulation_rank: rank of item in normalized circulation category
    :param total_items: number of items in same feature category
    """
    itemcount_score = rank_to_points(itemcount_rank, total_items)
    normalized_circulation_score = rank_to_points(
        normalized_circulation_rank, total_items)

    return {'itemcount_score': itemcount_score,
            'normalized_circulation_score': normalized_circulation_score,
            'total_score': itemcount_score + normalized_circulation_score,
            'stars': itemcount_score + normalized_circulation_score + 3
            }


def calculate_list_feature_score(feature_list, t):
    """
    Calculates feature score for genres/subjects (attribute score consist of array of features).

    :param feature_list: list of features
    :param t: type of features
    """
    feature_count = 0
    wp_features = 0
    bp_features = 0
    common_features = 0
    ml_features = 0
    new_features = 0

    for f in feature_list['items']:
        if 'new' in f.keys():
            new_features += 1
            continue

        if f['ml_feature']:
            ml_features += 1

        scores = calculate_feature_score(
            f['historical_itemcount_rank'], f['historical_circulation_normalized_rank'], f['total'])

        if scores['itemcount_score'] > 0:
            common_features += 1

        if scores['normalized_circulation_score'] > 0:
            wp_features += 1
        elif scores['normalized_circulation_score'] < 0:
            bp_features += 1

        feature_count += 1

    if t == 'Genre':
        total_score = wp_features + new_features - (round(bp_features * 0.5))
    else:
        total_score = wp_features + new_features - bp_features

    if total_score >= 2:
        stars = 5
    elif total_score <= -2:
        stars = 1
    else:
        stars = total_score + 3

    return {
        'feature_count': feature_count,
        'common_features': common_features,
        'wp_features': wp_features,
        'bp_features': bp_features,
        'ml_features': ml_features,
        'new_features': new_features,
        'total_score': stars - 3,
        'stars': stars
    }


def get_dnn_prediction(ml_pred_item, model, tokenizers, field_lengths):
    """
    Returns dnn prediction given the array of tokenizers and dnn model.

    :param ml_pred_item: Item-class object to make prediction from
    :param model: DNN model to use for making prediction
    :param tokenizers: array of tokenizers to be used to extract features from item
    """
    X1, X2, X3, X4, X5 = [[] for x in range(5)]
    author = tokenizers['author'].texts_to_sequences(
        [ml_pred_item.get_feature('authors')])[0]
    author = pad_sequence(author, field_lengths['authors'])
    X1.append(author)

    genres = tokenizers['genres'].texts_to_sequences(
        [ml_pred_item.get_feature('genres')])[0]
    genres = pad_sequence(genres, field_lengths['genres'])
    X2.append(genres)

    series = tokenizers['series'].texts_to_sequences(
        [ml_pred_item.get_feature('series')])[0]
    series = pad_sequence(series, field_lengths['series'])
    X3.append(series)

    subject = tokenizers['subjects'].texts_to_sequences(
        [ml_pred_item.get_feature('subjects')])[0]
    subject = pad_sequence(subject, field_lengths['subjects'])
    X4.append(subject)

    publisher = tokenizers['publisher'].texts_to_sequences(
        [ml_pred_item.get_feature('publishers')])[0]
    publisher = pad_sequence(publisher, field_lengths['publishers'])
    X5.append(publisher)

    X1 = np.array(X1)
    X2 = np.array(X2)
    X3 = np.array(X3)
    X4 = np.array(X4)
    X5 = np.array(X5)

    prediction = model.predict([X1, X2, X3, X4, X5])
    return np.argmax(prediction, axis=1)[0]


def get_resource_statistics(i, t, h, session, tokenizer):
    """
    Returns statistics regarding the input resource.

    :param i: item to get statistics from
    :param t: type of item
    :param h: label of heading in database
    :param session: database session
    :param tokenizer: tokenizer used to extract features
    """
    resource = session.query(eval(t)).filter(eval(t).id == i).first()

    if resource == None:
        return get_newitem_score(i, t)

    if t == 'Series':
        resources_by_historical_itemcount = session.query(eval(t).label, func.count(DBItem.id)).join(
            DBItem, eval(t).items).group_by(eval(t).id).order_by(func.count(DBItem.id).desc())
        resources_by_historical_circulation = calculate_totals(session.query(
            eval(t).label, DBItem.circulation_sequence).join(DBItem, eval(t).items).all())
        resource_item_data = session.query(DBItem.circulation_sequence).join(
            DBItem, eval(t).items).filter(eval(t).id == i, DBItem.deleted == None).all()
    else:
        resources_by_historical_itemcount = session.query(eval(f'{t}.{h}'), func.count(
            DBItem.id)).outerjoin(DBItem).group_by(eval(t).id).order_by(func.count(DBItem.id).desc())
        resources_by_historical_circulation = calculate_totals(session.query(
            eval(f'{t}.{h}'), DBItem.circulation_sequence).outerjoin(DBItem).all())
        resource_item_data = session.query(DBItem.circulation_sequence).filter(
            eval(f'DBItem.{t.lower()}_id') == resource.id, DBItem.deleted == None).all()

    resource_rank_historical_itemcount = [(x, y[1]) for x, y in enumerate(
        resources_by_historical_itemcount) if y[0] == getattr(resource, h)][0]
    resource_rank_historical_circulation = [(x, y[1]) for x, y in enumerate(
        resources_by_historical_circulation) if y[0] == getattr(resource, h)][0]

    resources_by_normalized_historical_circulation = calculate_normalized_totals(
        resources_by_historical_itemcount, resources_by_historical_circulation)
    resource_rank_normalized_historical_circulation = [(x, y[1]) for x, y in enumerate(
        resources_by_normalized_historical_circulation) if y[0] == getattr(resource, h)][0]

    resource_item_data = [x[0] for x in resource_item_data]
    resource_current_itemcount = len(resource_item_data)
    resource_trend = get_trend(resource_item_data, normalized=True)

    resource_score = calculate_feature_score(
        resource_rank_historical_itemcount[0], resource_rank_normalized_historical_circulation[0], len(resources_by_historical_circulation))

    if sum(resource_trend) <= 0 and resource_score['total_score'] > -2:
        resource_score['normalized_circulation_score'] -= 1
        resource_score['total_score'] -= 1
        resource_score['stars'] -= 1

    return {
        'heading': getattr(resource, h),
        'current_itemcount': resource_current_itemcount,
        'historical_itemcount': resource_rank_historical_itemcount[1],
        'historical_itemcount_rank': resource_rank_historical_itemcount[0] + 1,
        'historical_circulation': resource_rank_historical_circulation[1],
        'historical_circulation_rank': resource_rank_historical_circulation[0] + 1,
        'historical_circulation_normalized': resource_rank_normalized_historical_circulation[1],
        'historical_circulation_normalized_rank': resource_rank_normalized_historical_circulation[0] + 1,
        'normalized_trend': resource_trend,
        'total': len(resources_by_historical_circulation),
        'ml_feature': was_usable_feature(getattr(resource, h), tokenizer),
        'score': resource_score
    }


def get_listresource_statistics(i, t, h, session, tokenizer):
    """
    Returns statistics regarding the input resource (for joined arrays).

    :param i: items in array form
    :param t: type of items
    :param h: label of heading in database
    :param session: database session
    :param tokenizer: tokenizer used to extract features for ML prediction
    """
    ml_pred_resources = []
    resources = i.split(' ')
    res = {}
    res['items'] = []

    resources_by_historical_itemcount = session.query(eval(t).label, func.count(DBItem.id)).join(
        DBItem, eval(t).items).group_by(eval(t).id).order_by(func.count(DBItem.id).desc())
    resources_by_historical_circulation = calculate_totals(session.query(
        eval(t).label, DBItem.circulation_sequence).join(DBItem, eval(t).items).all())
    resources_by_normalized_historical_circulation = calculate_normalized_totals(
        resources_by_historical_itemcount, resources_by_historical_circulation)

    for r in resources:
        resource = session.query(eval(t)).filter(eval(t).id == r).first()
        if resource == None:
            res['items'].append(get_newitem_score(r, t))
            continue

        # This creates overhead - optimize this
        resource_rank_historical_itemcount = [(x, y[1]) for x, y in enumerate(
            resources_by_historical_itemcount) if y[0] == getattr(resource, h)][0]
        resource_rank_historical_circulation = [(x, y[1]) for x, y in enumerate(
            resources_by_historical_circulation) if y[0] == getattr(resource, h)][0]
        resource_rank_normalized_historical_circulation = [(x, y[1]) for x, y in enumerate(
            resources_by_normalized_historical_circulation) if y[0] == getattr(resource, h)][0]

        resource_item_data = session.query(DBItem.circulation_sequence).join(
            DBItem, eval(t).items).filter(eval(t).id == r, DBItem.deleted == None).all()
        resource_item_data = [x[0] for x in resource_item_data]
        resource_current_itemcount = len(resource_item_data)
        resource_trend = get_trend(resource_item_data, normalized=True)

        res['items'].append({
            'heading': getattr(resource, h),
            'current_itemcount': resource_current_itemcount,
            'historical_itemcount': resource_rank_historical_itemcount[1],
            'historical_itemcount_rank': resource_rank_historical_itemcount[0] + 1,
            'historical_circulation': resource_rank_historical_circulation[1],
            'historical_circulation_rank': resource_rank_historical_circulation[0] + 1,
            'historical_circulation_normalized': resource_rank_normalized_historical_circulation[1],
            'historical_circulation_normalized_rank': resource_rank_normalized_historical_circulation[0] + 1,
            'normalized_trend': resource_trend,
            'total': len(resources_by_historical_circulation),
            'ml_feature': was_usable_feature(getattr(resource, h), tokenizer)
        })

        ml_pred_resources.append(getattr(resource, h))

    return (res, ml_pred_resources)


def get_recommendation(args, session, tokenizers, classifier, field_lengths):
    """
    Wraps the overall recommendation process to a single function.

    :param args: item attributes/parameters for recommendation
    :param session: database session
    :param tokenizers: array of tokenizers used to extract features
    :param classifier: classifier for making ML prediction
    :param field_lengts: fields lengths for padding features
    """

    ml_pred_item = Item(authors=[], publishers=[], series=[],
                        pubyear=2020, genres=[], subjects=[])
    ml_pred_item.set_circulation_sequence([0])

    res = {}
    total_score = 0
    total_ml_features = 0

    if 'author' in args.keys():
        author_id = args['author']
        res['author'] = get_resource_statistics(
            author_id, 'Author', 'name', session, tokenizers['author'])

        if res['author']:
            total_score += res['author']['score']['total_score']
            if res['author']['ml_feature']:
                ml_pred_item.authors = [res['author']['heading']]
                total_ml_features += 1

    if 'publisher' in args.keys():
        publisher_id = args['publisher']
        res['publisher'] = get_resource_statistics(
            publisher_id, 'Publisher', 'name', session, tokenizers['publisher'])

        if res['publisher']:
            total_score += res['publisher']['score']['total_score']
            if res['publisher']['ml_feature']:
                ml_pred_item.publishers = [res['publisher']['heading']]
                total_ml_features += 1

    if 'series' in args.keys():
        series_id = args['series']
        res['series'] = get_resource_statistics(
            series_id, 'Series', 'label', session, tokenizers['series'])

        if res['series']:
            total_score += res['series']['score']['total_score']
            if res['series']['ml_feature']:
                ml_pred_item.series = [res['series']['heading']]
                total_ml_features += 1

    if 'genres' in args.keys():
        genres = args['genres']
        res['genres'], ml_pred_item.genres = get_listresource_statistics(
            genres, 'Genre', 'label', session, tokenizers['genres'])

        if res['genres']:
            genres_score = calculate_list_feature_score(res['genres'], 'Genre')
            total_score += genres_score['total_score']
            total_ml_features += genres_score['ml_features']
            res['genres']['score'] = genres_score

    if 'subjects' in args.keys():
        subjects = args['subjects']
        res['subjects'], ml_pred_item.subjects = get_listresource_statistics(
            subjects, 'Subject', 'label', session, tokenizers['subjects'])

        if res['subjects']:
            subjects_score = calculate_list_feature_score(
                res['subjects'], 'Subject')
            total_score += subjects_score['total_score']
            total_ml_features += subjects_score['ml_features']
            res['subjects']['score'] = subjects_score

    # ML pred requires minimum amount of available features and certainty
    if total_ml_features >= MIN_ML_PRED_FEATURES:
        ml_pred = get_dnn_prediction(ml_pred_item, classifier, tokenizers, field_lengths)
        res['ml'] = {'prediction': int(ml_pred)}

        if ml_pred == 1:
            total_score += 1
        else:
            total_score -= 1

    res['recommendation_score'] = total_score

    return res
