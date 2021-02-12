# FILE INFORMATION

# Location of data source files
ITEM_INFO_FILE_PATH = 'data/items.csv'
CIRCULATION_FILE_PATH = 'data/circulation.csv'

# Locations to save data during processing
PREPROCESS_FILE_PATH = {
    'training': 'data/preprocessed_training.pkl',
    'validating': 'data/preprocessed_validating.pkl',
    'testing': 'data/preprocessed_testing.pkl',
    'db_constructing': 'data/preprocessed_visualization.pkl'
}
MODEL_SAVE_FOLDER = 'models'

# DATA SPLIT
# Try to aim for (80/10/10) split for your data. Even if you don't plan to do
# development, take care that every split is valid as all of them affect the
# system when it's run. By default all data is used for training.

# DATA_START parameters:
# - Training should start the year/month circulation log starts and from ther
#   you can calculate when validating/testing should start
DATA_START_YEAR = {
    'training': 2014,
    'validating': 2018,
    'testing': 2019,
    'db_constructing': 1678  # DO NOT CHANGE THIS
}

DATA_START_MONTH = {
    'training': 7,
    'validating': 8,
    'testing': 4,
    'db_constructing': 1  # DO NOT CHANGE THIS
}

# DATA_END parameters:
# - Calculate values for training, validating and testing according to your data.
# - db_constructing should have the value of last full circulation log month
# - db_constructing value should be same as testing value here if you just want to deploy

DATA_END_MONTH = {
    'training': 7,
    'validating': 3,
    'testing': 9,
    'db_constructing': 3
}

DATA_END_YEAR = {
    'training': 2018,
    'validating': 2019,
    'testing': 2019,
    'db_constructing': 2019
}

# When does circulation log data start?
CIRCULATION_LOG_START_MONTH = 7
CIRCULATION_LOG_START_YEAR = 2014

# When does the circulation log data end?
# i.e. when did you ran the SQL queries?
DATA_OBTAINED_MONTH = 9
DATA_OBTAINED_YEAR = 2020

# Data filtering, by default you should not need to
# change any of these
NO_RENEWALS = True
MIN_ITEM_SUBJECTS = 3
MIN_MONTHS_CIRCULATED = 2
MIN_FEATURES = 5
MONTHS_TO_AVG = 12
CIRCULATION_CLASSIFICATION_BREAKPOINT = 4/12

# FINNA
# If you are using Finna you should check these parameters
# If you are not using Finna, just turn USE_FINNA to False
USE_FINNA = True
FORCE_FETCH = False
FINNA_FILE_PATH = 'data/finna_data.json'
FINNA_LIBRARY_NAME = 'vaarakirjastot'
SUBJECT_SOURCES = [
    'kaunokki', 'ysa', 'kauno7fin', 'kaunokki.', ' kauno/fin', 'yso/fin', 'yso', 'kaunokkki', 
    'kauno/fin', 'kaunu/fin', 'kauni/fin', 'ykauno/fin', 'kauno/fi', 'kaun/fin'
    ]
CONTACT_EMAIL = ''

# Symbols
SEQUENCE_DELETED_SYMBOL = -1  # DO NOT CHANGE

# ML hyperparameters
EPOCHS = 30
LEARNING_RATE = 0.001
