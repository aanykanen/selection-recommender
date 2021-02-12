# Backend
Backend service consists of an API that serves processed information. Sources for the processed information are a local database that is constructed during the building phase and a machine learning model that is trained during the building phase. The API service is handled by a simple Flask app.

## Backend dependencies

Copy of Apache License Version 2 is included in the repository with name apache2_LICENSE as Tensorflow, XgBoost and Request libraries are licensed under the Apache license version 2.

- Name: NumPy
    - License: <a href="https://github.com/numpy/numpy/blob/master/LICENSE.txt">BSD 3-clause license</a>

- Name: Pandas
    - License: <a href="https://github.com/pandas-dev/pandas/blob/master/LICENSE">BSD 3-clause license</a>

- Name: Matplotlib
    - License: <a href="https://github.com/matplotlib/matplotlib/blob/master/LICENSE/LICENSE">Matplotlib license</a>

- Name: SQLAlchemy
    - License: <a href="https://github.com/sqlalchemy/sqlalchemy/blob/master/LICENSE">MIT license</a>

- Name: Flask
    - License: <a href="https://github.com/pallets/flask/blob/master/LICENSE.rst">BSD 3-clause license</a>

- Name: Flask-cors
    - License: <a href="https://github.com/corydolphin/flask-cors/blob/master/LICENSE">MIT license</a>

- Name: Flask-restful
    - License: <a href="https://github.com/flask-restful/flask-restful/blob/master/LICENSE">BSD 3-clause license</a>

- Name: Flask-marshmallow
    - License: <a href="https://github.com/marshmallow-code/flask-marshmallow/blob/dev/LICENSE">MIT license</a>

- Name: Flask-sqlalchemy
    - License: <a href="https://github.com/pallets/flask-sqlalchemy/blob/master/LICENSE.rst">BSD 3-clause license</a>

- Name: Flask-SQLAlchemy-session
    - License: <a href="https://github.com/dtheodor/flask-sqlalchemy-session/blob/master/LICENSE">MIT license</a>

- Name: Tensorflow
    - License: <a href="https://github.com/tensorflow/tensorflow/blob/master/LICENSE">Apache license 2.0</a>

- Name: Sklearn
    - License: <a href="https://github.com/scikit-learn/scikit-learn/blob/main/COPYING">BSD 3-clause license</a>

- Name: Lightgbm
    - License: <a href="https://github.com/microsoft/LightGBM/blob/master/LICENSE">MIT license</a>

- Name: XgBoost
    - License: <a href="https://github.com/dmlc/xgboost/blob/master/LICENSE">Apache license 2.0</a>

- Name: Seaborn
    - License: <a href="https://github.com/mwaskom/seaborn/blob/master/LICENSE">BSD 3-clause license</a>

- Name: Requests
    - License: <a href="https://github.com/psf/requests/blob/master/LICENSE">Apache license 2.0</a>
  - Notice file: is appended to the NOTICE file found in this folder


## Building the backend
There are multiple phases that are done during the building stage of the backend. Some phases, especially the database building, may take a long period of time (tested with ~50k records, it took 7 hours). Before that phase has been either tested with larger datasets or optimized, I would suggest against deploying the app with large collections. 

The main phases of building the backend are:
1. Preprocessing data
2. Building a local database
3. Training a machine learning classifier
4. Starting the API service

### 1. Preprocessing data
This version can preprocess the data only from .csv-files that have been acquired from Koha database using the SQL-queries in the sql-folder or have similar format than what these queries output. The queries are developed for Koha version 17.05 database schema and might not support other versions of the schema.

At this point, create a new virtual environment for Python (use for example pipenv or virtualenv) and install the required packages. **All python scripts need to be run from the backend folder**.

The first task before running any of the scripts is to set date configurations correctly to ml/ml_conf.py. Variables DATA_START_MONTH, DATA_START_YEAR, DATA_END_MONTH and DATA_END_YEAR need to have proper values in them. Data start times for training data should match the date when circulation logs have started and data end times for test data should match the date when data was extracted from the database using the SQL queries. These variables control multiple important things, such as the generation of circulation sequences, so the importance of proper configuration is really a matter of the system working as designed. By default the integration with Finnish Finna service is disabled. This can be enabled from the configuration file if your library has materials available in Finna and is able to gather the metadata using Finna API. In this case you need to configure USE_FINNA, FINNA_LIBRARY_NAME and CONTACT_EMAIL variables. The contact email is used only for the headers of the API calls for Finna API service.

The preprocessing starts with concatenating the files containing item information and circulation logs with help of the script (data/combine_csv.sh). This script outputs two files: items.csv and circulation.csv. After this the script ml/preprocess_data.py needs to be run. This script preprocesses the data and generates serialized files that that are used in training the machine learning model and constructing the database.

### 2. Building the database / 3. Training the machine learning classifier
At this step you may choose to either construct the database using ml/build_db.py script or train the machine learning model. The database building will take a lot longer so you may also start that and let it run on the background. While at first it seems the database building is quick, it slows down after around ~3k records have been imported because of how many links there are in the data. If you wish to just train the machine learning model with default parameters you can run the file ml/lightgbm_train.py and it will train the machine learning model and save it to models folder.  If you want to compare how well different models make predictions with your dataset you can run first the ml/dnn_train.py to train the dnn network and afterwards run the ml/compare_ml_models.py to compare the accuracies between different models. The comparison script saves metrics to metrics folder.

### 4. Starting the API service
After the database has been build and the lightgbm model has been trained you can start the api/api.py to serve the development version of the API.

### TL;DR
1. Make sure you executed SQL queries and they produced four files with correct columns. 
    - If Koha version != 17.05 check that queries are compatible with database schema of the version you are using.
2. Make sure configurations are right in ml/ml_conf.py
3. Create a new virtual environment with Python 3.8 and install required packages.
4. Place the four .csvs to data folder. Run combine_csv.sh

**Run python scripts from inside the backend folder. I.e. cd inside the folder where this README is located**

5. Run ml/preprocess_data.py
6. Run ml/lightgbm_train.py
7. Run ml/build_db.py (takes long time)
8. Run api/api.py and keep in mind this runs a dev server

## Known issues
- Database building takes forever. Graph databases or other types of solutions should be investigated as an alternative for SQLite.
- There is certainly room for improvement in ML model prediction accuracy.
- Data gathering methods are suboptimal. SQL queries are lacking and Finna OAI-PMH harvesting would be better option to use than Finna API.
