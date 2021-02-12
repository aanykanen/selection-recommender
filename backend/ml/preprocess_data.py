import os
import pickle
import sys

from multiprocessing import Pool

from ml_conf import *
from preprocess_utils import finna_api_fetch, load_item_data, preprocess_items, process_phase


if __name__ == "__main__":
    """
    This script preprocesses the data and saves it in serialized form. 
    It requires both items.csv and circulation.csv to be valid and present in the configured location 
    (by default data/ folder). Configurations from ml_conf.py are used
    so be sure to make configurations accordingly based on your data before running the script.
    """
    print('\nStarting data preprocessing with following configuration:')
    print(f'  * File regarding item information: {ITEM_INFO_FILE_PATH}')
    print(f'  * File regarding circulation information: {CIRCULATION_FILE_PATH}')
    print(f'  * Using Finna API: {USE_FINNA}')
    print(f'  * Forcing fetch from Finna API also if cached version exists: {FORCE_FETCH}\n')

    if not os.path.isfile(ITEM_INFO_FILE_PATH):
        print(f'File {ITEM_INFO_FILE_PATH} containing item information was not found. Exiting.')
        sys.exit(1)

    if not os.path.isfile(CIRCULATION_FILE_PATH):
        print(f'File {CIRCULATION_FILE_PATH} containing circulation information was not found. Exiting.')
        sys.exit(1)

    df_info, _ = load_item_data()

    if USE_FINNA:
        if not os.path.isfile(FINNA_FILE_PATH) or FORCE_FETCH:
            if FORCE_FETCH:
                print('Forcing a data update from Finna')
            else:
                print('Did not find Finna data from cache')

            ids = list(set([int(x) for x in df_info['bib_id'].tolist() if x != '\\N']))
            finna_api_fetch(ids, FINNA_LIBRARY_NAME)
        else:
            print('Finna items already fetched, using these items')

    print()
    with Pool() as p:
        p.map(process_phase, PREPROCESS_FILE_PATH.keys())
