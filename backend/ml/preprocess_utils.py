import calendar
import copy
import datetime
import json
import math
import pickle
import re
import sys
import time

import requests
import pandas as pd
import numpy as np

from multiprocessing import current_process

sys.path.append('..')
from backend.classes.item import Item
from ml_conf import *


def calculate_diff_month(d1, d2):
    """
    Calculates amount of months between two dates

    :param d1: date to calculate time between from
    :param d2: date to calculate time between to
    """
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def finna_api_fetch(ids, library):
    """
    Fetches item data from Finna API and saves it to disk

    :param ids: array of bib ids
    :param library: library name as identified in Finna
    """
    unfetched = copy.deepcopy(ids)
    results = []
    error_urls = []
    base_url = 'https://api.finna.fi/api/v1/record?'

    error_fp = f'{FINNA_FILE_PATH.split(".")[0]}_errors.json'
    error_count = 0

    print('Starting fetching data from Finna API\n')
    while len(unfetched) > 0:
        url = base_url

        # Retrieving 100 records in one request per Finna administration recommendation
        for i in range(100):
            url += f'id[]={library}.{str(unfetched[0])}&'
            del unfetched[0]

            if len(unfetched) == 0:
                break

        url += 'field[]=classifications&' \
            'field[]=container&' \
            'field[]=genres&' \
            'field[]=id&' \
            'field[]=newerTitles&' \
            'field[]=previousTitles&' \
            'field[]=nonPresenterAuthors' \
            '&field[]=rating' \
            '&field[]=series' \
            '&field[]=shortTitle' \
            '&field[]=subjectsExtended' \
            '&field[]=publishers&' \
            'field[]=summary&' \
            'field[]=year&' \
            'lng=fi'

        headers = {'from': CONTACT_EMAIL}
        res = requests.get(url, headers=headers)

        if res.status_code == 200:
            res = res.json()
        else:
            error_urls.append(url)
            error_count += 1
            continue

        if res['resultCount'] == 0:
            error_urls.append(url)
            error_count += 1
            continue

        records = res['records']
        results.extend(records)

        print('Waiting 5 seconds to not overburden the API')
        for i in range(5):
            print('.', end='')
            time.sleep(1)
        print()

        api_calls_left = math.ceil(len(unfetched) / 100)

        if api_calls_left > 0:
            print(f'\n{api_calls_left} API calls until all data is fetched')
            print(f'Estimating it takes another {round(api_calls_left / 12, 2)} minutes to complete')
        else:
            print('Data gathering from Finna API has finished!')

    results = {'records': results}
    error_urls = {'errorUrls': error_urls}
    json.dumps(results)
    json.dumps(error_urls)

    with open(FINNA_FILE_PATH, 'w') as fout:
        json.dump(results, fout)

    with open(error_fp, 'w') as fout:
        json.dump(error_urls, fout)

    print(f'\nFinna data was successfully saved to {FINNA_FILE_PATH}')
    print(f'Encountered {error_count} errors, check urls from {error_fp}')


def preprocess_basic_textual_data(data):
    """
    Preprocesses textual data with no extra requirements

    :param data: string to preprocess
    """
    data = (data
            .replace('[', '')
            .replace(']', '')
            .replace(',', '')
            .replace('.', '')
            .replace(';', '')
            .lower()
            .strip()
            )

    if data == '\\n':
        raise ValueError('Empty data was not filtered properly during preprocessing')

    return [data]


def parse_local_genre(location):
    """
    Takes local itemcallnumber as input, outputs textual description of genre based on the itemcallnumber.
    Currently supports only limited amount of classifications from Finnish Public Libraries Classification System class number 84.2.
    In future versions support for MARC field 655 should be added to SQL queries and this function should be expanded into a
    configuration file.

    :param location: itemcallnumber as a string
    """

    pattern = r'84.2\S*'
    match = re.search(pattern, location)

    if match is None:
        raise ValueError('Itemcallnumber type not supported currently')
    else:
        col = match.group()
        if col == '84.2' or col == '84.22':
            return 'romaanit'
        elif col == '84.23':
            return 'vironkielinen kaunokirjallisuus'
        elif col == '84.2DEK':
            return 'rikoskirjallisuus'
        elif col == '84.2ERÄ':
            return 'eräkertomukset'
        elif col == '84.2FAN':
            return 'fantasiakirjallisuus'
        elif col == '84.2HUU':
            return 'huumori'
        elif col == '84.2JÄN':
            return 'jännityskirjallisuus'
        elif col == '84.2KAS':
            return 'kasku'
        elif col == '84.2KAU':
            return 'kauhukirjallisuus'
        elif col == '84.2NOV':
            return 'novellit'
        elif col == '84.2RAK' or col == '84.2ROM':
            return 'rakkausromaanit'
        elif col == '84.2SCI':
            return 'tieteiskirjallisuus'
        elif col == '84.2SEL':
            return 'selkokirjat'
        elif col == '84.2SOT':
            return 'sotakirjallisuus'
        elif col == '84.2USK':
            return 'uskonnollinen kirjallisuus'
        else:
            print(f'Genre {col} not listed!')
            return 'romaanit'


def preprocess_series(series):
    """
    Preprocesses series information by doing the normal basic textual data
    preprocessing and in addition stripping other pieces of information that
    prevented linking entities. This function should be revised based on your
    data.

    :params series: series information as a string
    """
    dot = series.find('.')

    if dot > -1:
        series = series[:dot]

    series = (series
              .replace('[', '')
              .replace(']', '')
              .replace('&amp;', '')
              .replace(',', '')
              .replace('.', '')
              .replace(';', '')
              .replace('+', '')
              .replace('-sarja', '')
              .lower()
              .strip()
              )

    return [series]


def parse_sequence(df, item_id, acquired, deleted):
    """
    Parses circulation sequence from dataframe containing circulation log.

    :param df: dataframe containing circulation log
    :param item_id: id of item to parse
    :param acquired: date of acquisition of item
    :param deleted: date of deletion of item
    """
    circ = df.loc[df['item_id'] == item_id]
    first_circ_event = circ.datetime.min()
    last_circ_event = circ.datetime.max()
    data_end_last_day = calendar.monthrange(DATA_OBTAINED_YEAR, DATA_OBTAINED_MONTH)[1]
    bins = circ.groupby(pd.Grouper(key='datetime', freq='M')).count()
    data_start_datetime = datetime.date(CIRCULATION_LOG_START_YEAR, CIRCULATION_LOG_START_MONTH, 1)
    data_end_datetime = datetime.date(DATA_OBTAINED_YEAR, DATA_OBTAINED_MONTH, data_end_last_day)

    deleted = deleted if deleted != '' else None

    # Sanity check: Drop bins earlier than data start or later than data end
    bins = bins[(bins.index >= pd.Timestamp(CIRCULATION_LOG_START_YEAR, CIRCULATION_LOG_START_MONTH, 1)) & (
                bins.index <= pd.Timestamp(DATA_OBTAINED_YEAR, DATA_OBTAINED_MONTH, data_end_last_day))]

    # Sanity check: First circulation event is in data date range
    if first_circ_event != None and first_circ_event < data_start_datetime:
        first_circ_event = data_start_datetime
    elif first_circ_event > data_end_datetime:
        first_circ_event = data_end_datetime

    # Sanity check: Last circulation event is in data date range
    if last_circ_event != None and last_circ_event < data_start_datetime:
        last_circ_event = data_start_datetime
    elif last_circ_event > data_end_datetime:
        last_circ_event = data_end_datetime

    # Case: item has been borrowed at some point in data date range
    if not bins.empty:
        np_sequence = bins.to_numpy(dtype=np.int64).flatten()

        # Fill months without circulation between acquisition and first issue OR data start and first issue if acquired before
        # the circulation data starts
        if acquired.year >= CIRCULATION_LOG_START_YEAR + 1 or (acquired.month > CIRCULATION_LOG_START_MONTH and acquired.year == CIRCULATION_LOG_START_YEAR):
            months_to_fill_start = calculate_diff_month(first_circ_event, pd.Timestamp(acquired.year, acquired.month, acquired.day))
        else:
            months_to_fill_start = calculate_diff_month(first_circ_event, pd.Timestamp(CIRCULATION_LOG_START_YEAR, CIRCULATION_LOG_START_MONTH, 1))

        if months_to_fill_start > 0:
            np_sequence = np.concatenate([np.zeros(months_to_fill_start, dtype=np.int64), np_sequence])

        # Calculate zeros to fill to the end of sequence
        if deleted != None:
            months_to_fill_end = calculate_diff_month(pd.Timestamp(deleted.year, deleted.month, deleted.day), last_circ_event)
        else:
            months_to_fill_end = calculate_diff_month(pd.Timestamp(DATA_OBTAINED_YEAR, DATA_OBTAINED_MONTH, data_end_last_day), last_circ_event)

        if months_to_fill_end > 0:
            np_sequence = np.append(np_sequence, np.zeros(months_to_fill_end, dtype=np.int64))

    # Case: item has not been borrowed at any point in data date range
    else:
        # If the item was acquired after from where the circulation data starts
        if acquired.year >= CIRCULATION_LOG_START_YEAR + 1 or (acquired.month > CIRCULATION_LOG_START_MONTH and acquired.year == CIRCULATION_LOG_START_YEAR):
            if deleted != None:
                empty_amount = calculate_diff_month(
                    pd.Timestamp(deleted.year, deleted.month, deleted.day), 
                    pd.Timestamp(acquired.year, acquired.month, acquired.day))
                empty_amount += 1
            else:
                empty_amount = calculate_diff_month(
                    pd.Timestamp(DATA_OBTAINED_YEAR, DATA_OBTAINED_MONTH, 1), 
                    pd.Timestamp(acquired.year, acquired.month, acquired.day))
                empty_amount += 1
        else:
            if deleted != None:
                empty_amount = calculate_diff_month(
                    pd.Timestamp(deleted.year, deleted.month, deleted.day), 
                    pd.Timestamp(CIRCULATION_LOG_START_YEAR, CIRCULATION_LOG_START_MONTH, 1))
                empty_amount += 1
            else:
                empty_amount = calculate_diff_month(
                    pd.Timestamp(DATA_OBTAINED_YEAR, DATA_OBTAINED_MONTH, 1), 
                    pd.Timestamp(CIRCULATION_LOG_START_YEAR, CIRCULATION_LOG_START_MONTH, 1))
                empty_amount += 1

        np_sequence = np.zeros(empty_amount, dtype=np.int64)

    # Value -1 to the month when item was been deleted
    if deleted != None:
        np_sequence = np.append(
            np_sequence[:-1].copy(), np.array([SEQUENCE_DELETED_SYMBOL], dtype=np.int64))

    # Sanity check: Sequence length cant exceed the period from circulation log start to data obtained
    if len(np_sequence) > calculate_diff_month(datetime.date(DATA_OBTAINED_YEAR, DATA_OBTAINED_MONTH, 1), datetime.date(CIRCULATION_LOG_START_YEAR, CIRCULATION_LOG_START_MONTH, 1)) + 1:
        RuntimeError(
            'Sequence exceeds the maximum sequence length given the time period between data start and end date')

    # Sanity check: Sequence of deleted items ends correctly
    if deleted != None and np_sequence[-1] != -1:
        RuntimeError('Sequence of deleted item does not end in -1')

    return np_sequence


def load_finna_data():
    """
    Loads data file that was retrieved from Finna API earlier.
    """
    with open(FINNA_FILE_PATH, 'r') as fin:
        data = fin.read()

    data = json.loads(data)
    return data['records']


def load_item_data():
    """
    Loads item and circulation data from preprocessed files.
    """
    try:
        df_info = pd.read_csv(ITEM_INFO_FILE_PATH, header=None, index_col=False, low_memory=False)
        df_circulation = pd.read_csv(CIRCULATION_FILE_PATH, header=None, index_col=False)

        info_column_names = ['bib_id', 'item_id', 'author', 'title']
        for i in range(1, 16):
            info_column_names.append(f'subject_{i}')
            info_column_names.append(f'subject_{i}_source')

        info_column_names.extend(['series', 'genre', 'isbn', 'pub_year',
                                  'acquired', 'last_borrowed', 'issues', 'renewals', 'date_deleted'])
        df_info.columns = info_column_names

        df_circulation.columns = ['item_id', 'datetime', 'type']

    except Exception as e:
        print('Problem in reading input files. Please check that item info and circulation .csv files are valid.')
        print(f'Full error message was the following:\n {e}')
        sys.exit(1)

    return df_info, df_circulation


def preprocess_items(phase):
    """
    Preprocesses items given the phase. Each phase is configured in conf.py file.

    :param phase: phase of processing
    """
    df_info, df_circulation = load_item_data()

    if NO_RENEWALS:
        df_circulation.drop(df_circulation[df_circulation.type != 'issue'].index, inplace=True)

    df_circulation.drop(columns=['type'], inplace=True)
    df_circulation['datetime'] = pd.to_datetime(
        df_circulation['datetime'], format='%Y-%m-%d %H:%M:%S')

    if USE_FINNA:
        finna_data = load_finna_data()

    items = []

    for i in df_info.iterrows():
        if USE_FINNA:
            item = preprocess_finna_data(phase, i, df_circulation, finna_data)
        else:
            item = preprocess_local_data(phase, i, df_circulation)

        if item is None:
            continue

        circ_seq = parse_sequence(
            df_circulation, i.item_id, item.acquired, item.deleted).tolist()

        item.set_circulation_sequence(circ_seq)
        items.append(item)

    return items


def preprocess_local_data(phase, item, df_circulation):
    """
    Preprocesses item using data from .csv files.

    :param phase: phase of preprocessing
    :param item: item to prepreprocess
    :param df_circulation: dataframe containing circulation log
    """
    author = preprocess_basic_textual_data(item.author) if (item.author == item.author and item.author != '\\N') else []
    title = item.title
    series = preprocess_series(item.series) if item.series == item.series else []
    acquired = datetime.datetime.strptime(item.acquired, '%Y-%m-%d')
    deleted = datetime.datetime.strptime(item.date_deleted, '%Y-%m-%d %H:%M:%S') if item.date_deleted == item.date_deleted else None

    # Thanks datapoints such as 2013-00-01
    try:
        last_borrowed = datetime.datetime.strptime(item.last_borrowed, '%Y-%m-%d') if item.last_borrowed == item.last_borrowed else None
    except:
        last_borrowed = None

    pubyear = item.pub_year if item.pub_year != '\\N' else None
    genre = [parse_local_genre(item.genre)]
    subjects = []

    for i in range(15):
        subject = item.loc[f'subject_{i+1}']
        if subject == subject and subject != '\\N':
            subjects.append(preprocess_basic_textual_data(subject)[0])

    return Item(
        bib_id=item.bib_id, 
        item_id=item.item_id, 
        authors=author, 
        title=title, 
        publishers=[], 
        series=series, 
        pubyear=pubyear, 
        acquired=acquired, 
        deleted=deleted, 
        genres=genre, 
        subjects=subjects, 
        last_borrowed=last_borrowed)


def preprocess_finna_data(phase, item, df_circulation, finna_data):
    """
    Preprocesses item using data retrieved from Finna.

    :param phase: phase of preprocessing
    :param item: item to be preprocessed
    :param df_circulation: dataframe containing circulation log
    :param finna_data: data retrieved from finna
    """
    bib_id = item.bib_id if item.bib_id != '\\N' else -1
    item_id = item.item_id if item.item_id != '\\N' else -1

    # Bib id, item id and acquisition date must be valid
    if bib_id == -1 or item_id == -1 or item.acquired == '\\N':
        return None

    acquired = datetime.datetime.strptime(item.acquired, '%Y-%m-%d')
    deleted = datetime.datetime.strptime(item.date_deleted, '%Y-%m-%d %H:%M:%S') if item.date_deleted == item.date_deleted else None
    
    try:
        last_borrowed = datetime.datetime.strptime(item.last_borrowed, '%Y-%m-%d') if item.last_borrowed == item.last_borrowed else None
    except:
        last_borrowed = None

    finna_record = list(filter(lambda x: x["id"] == f'{FINNA_LIBRARY_NAME}.{bib_id}', finna_data))

    # Drop items acquired after data end
    if acquired.year > DATA_END_YEAR[phase] or (acquired.year == DATA_END_YEAR[phase] and acquired.month > DATA_END_MONTH[phase]):
        return None

    # Drop items acquired before data start
    if acquired.year < DATA_START_YEAR[phase] or (acquired.year == DATA_START_YEAR[phase] and acquired.month < DATA_START_MONTH[phase]):
        return None

    # Local info serves as fallback if record is not found from Finna
    if not len(finna_record) > 0:
        return preprocess_local_data(phase, item, df_circulation)

    finna_record = finna_record[0]

    author = preprocess_basic_textual_data(
        finna_record['nonPresenterAuthors'][0]['name']) if len(finna_record['nonPresenterAuthors']) > 0 else []
    title = finna_record['shortTitle']
    publishers = [preprocess_basic_textual_data(x)[0] for x in finna_record['publishers']]
    pubyear = int(finna_record['year'])
    series = [preprocess_series(x['name'])[0] for x in finna_record["series"]]
    genres = [preprocess_basic_textual_data(x)[0] for x in finna_record["genres"]]
    subjects = []

    if 'subjectsExtended' in finna_record.keys():
        for i in finna_record['subjectsExtended']:
            if 'source' in i.keys() and i['source'] in SUBJECT_SOURCES:
                subjects.extend([preprocess_basic_textual_data(x)[0] for x in i['heading']])

    return Item(
        bib_id=bib_id, 
        item_id=item_id, 
        authors=author, 
        title=title, 
        publishers=publishers, 
        series=series, 
        pubyear=pubyear, 
        acquired=acquired, 
        deleted=deleted, 
        genres=genres, 
        subjects=subjects, 
        last_borrowed=last_borrowed)


def process_phase(phase):
    """
    Helper function for multiprocessing.

    :param phase: phase of processing
    """
    items = preprocess_items(phase)
    pickle.dump(items, open(PREPROCESS_FILE_PATH[phase], 'wb'))
