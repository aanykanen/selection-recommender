import functools
import json
import os
import operator

import matplotlib.pyplot as plt
import numpy as np


def produce_metrics(data, bins, ticks, phase):
    """
    Saves histograms of values given to each attribute in a list of recommendations.
    Useful for checking distributions when tuning the rules of overall recommender system.

    :param data: recommendation data in array form
    :param bins: number of bins for histogram
    :param ticks: number of ticks in X axis for histogram
    :phase phase: name of phase of processing (e.g. validating)
    """
    print('Some key metrics from test set\n')
    print(f'Number of items in test set: {len(data)}\n')

    author_info = len([1 for x in data if 'author' in x.keys()])
    author_scores = [x['author']['score']['total_score'] for x in data if 'author' in x.keys()]
    author_uniq = len(set([x['author']['heading'] for x in data if 'author' in x.keys()]))
    author_new = [x['author']['heading'] for x in data if 'author' in x.keys() and 'new' in x['author'].keys()]
    count_author_new = len(set(author_new))
    print(f'Number of items containing author info: {author_info}')
    print(f'Number of unique authors: {author_uniq}')
    print(f'Number of new authors: {count_author_new}\n')

    series_info = len([1 for x in data if 'series' in x.keys()])
    series_scores = [x['series']['score']['total_score'] for x in data if 'series' in x.keys()]
    series_uniq = len(set([x['series']['heading'] for x in data if 'series' in x.keys()]))
    series_new = [x['series']['heading'] for x in data if 'series' in x.keys() and 'new' in x['series'].keys()]
    count_series_new = len(set(series_new))
    print(f'Number of items containing series info: {series_info}')
    print(f'Number of unique series: {series_uniq}')
    print(f'Number of new series: {count_series_new}\n')

    publisher_info = len([1 for x in data if 'publisher' in x.keys()])
    publisher_scores = [x['publisher']['score']['total_score'] for x in data if 'publisher' in x.keys()]
    publishers_uniq = len(set([x['publisher']['heading'] for x in data if 'publisher' in x.keys()]))
    publishers_new = [x['publisher']['heading'] for x in data if 'publisher' in x.keys() and 'new' in x['publisher'].keys()]
    count_publishers_new = len(list(set(publishers_new)))
    print(f'Number of items containing publisher info: {publisher_info}')
    print(f'Number of unique publishers: {publishers_uniq}')
    print(f'Number of new publishers: {count_publishers_new}\n')

    subject_info = len([1 for x in data if 'subjects' in x.keys()])
    subject_scores = [x['subjects']['score']['total_score'] for x in data if 'subjects' in x.keys()]
    all_subjects = [x['subjects']['items'] for x in data if 'subjects' in x.keys()]
    all_subjects = functools.reduce(operator.iconcat, all_subjects, [])
    subjects_uniq = len(set([x['heading'] for x in all_subjects]))
    count_subjects_new = len(set([x['heading'] for x in all_subjects if 'new' in x.keys()]))
    print(f'Number of items containing subject info: {subject_info}')
    print(f'Number of unique subjects: {subjects_uniq}')
    print(f'Number of new subjects: {count_subjects_new}\n')

    genres_info = len([1 for x in data if 'genres' in x.keys()])
    genre_scores = [x['genres']['score']['total_score'] for x in data if 'genres' in x.keys()]
    all_genres = [x['genres']['items'] for x in data if 'genres' in x.keys()]
    all_genres = functools.reduce(operator.iconcat, all_genres, [])
    genres_uniq = len(set([x['heading'] for x in all_genres]))
    count_genres_new = len(set([x['heading'] for x in all_genres if 'new' in x.keys()]))
    print(f'Number of items containing genres info: {genres_info}')
    print(f'Number of unique genres: {genres_uniq}')
    print(f'Number of new genres: {count_genres_new}\n')

    ml_scores = [x['ml']['prediction'] for x in data if 'ml' in x.keys()]
    print(f'Number of ML predictions: {len(ml_scores)}')
    print(f'Number of class 0 predictions: {ml_scores.count(0)}')
    print(f'Number of class 1 predictions: {ml_scores.count(1)}')
    recommendation_scores = [x['recommendation_score'] for x in data]

    def save_histogram(data, name):
        plt.hist(data, bins=bins)
        plt.xticks(ticks)
        plt.savefig(f'metrics/rs_metrics/{name}_{phase}_histogram.png')
        plt.clf()

    save_histogram(author_scores, 'author')
    save_histogram(series_scores, 'series')
    save_histogram(publisher_scores, 'publisher')
    save_histogram(subject_scores, 'subject')
    save_histogram(genre_scores, 'genre')
    save_histogram(ml_scores, 'ml_scores')
    save_histogram(recommendation_scores, 'recommendation')


if __name__ == "__main__":
    """
    This script produces attribute-level metrics from the data
    acquired through testing the full recommender system.
    """
    with open('metrics/rs_results.json') as f:
        data = json.load(f)

    if not os.path.exists('metrics/rs_metrics'):
        os.makedirs('metrics/rs_metrics')

    bins = np.arange(6) - 2.5
    x_ticks = np.arange(6) - 2

    phase = 'validating'
    produce_metrics(data, bins, x_ticks, phase)
