import numpy as np
import numbers
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import datetime
import taos
import pandas as pd
from sklearn.metrics import roc_auc_score
from sklearn.preprocessing import StandardScaler
import argparse
from sklearn.utils import check_array


def insert_demo_data(conn, consur, database, table, ground_truth_flag):
    '\n    Inserting demo_data. Monitoring the process of database operations with to create a database and table, with time stamps.\n\n    Parameters\n    ----------\n    conn: taos.connection.TDengineConnection\n        TDEnginine connection name.\n    cursor: taos.cursor.TDengineCursor\n        TDEnginine cursor name.\n    database: str\n        Connect database name.\n    table: str\n        Table to query from.\n    ground_truth_flag: bool, optional (default=False)\n        Whether uses ground truth to evaluate the performance or not.\n\n    Returns\n    -------\n    ground_truth: numpy array\n        The ground truth numpy array.\n\n    '
    try:
        consur.execute(('drop database if exists %s' % database))
        consur.execute(('create database if not exists %s' % database))
    except Exception as err:
        conn.close()
        raise err
    try:
        consur.execute(('use %s' % database))
    except Exception as err:
        conn.close()
        raise err
    try:
        consur.execute(('create table if not exists %s (ts timestamp, a float, b float)' % table))
    except Exception as err:
        conn.close()
        raise err
    start_time = datetime.datetime(2019, 8, 1)
    time_interval = datetime.timedelta(seconds=60)
    for _ in range(200):
        try:
            consur.execute(("insert into %s values ('%s', %f, %f,)" % (table, start_time, ((0.3 * np.random.randn(1)) - 2), ((0.3 * np.random.randn(1)) - 2))))
        except Exception as err:
            conn.close()
            raise err
        start_time += time_interval
    for _ in range(200):
        try:
            consur.execute(("insert into %s values ('%s', %f, %f,)" % (table, start_time, ((0.3 * np.random.randn(1)) + 2), ((0.3 * np.random.randn(1)) + 2))))
        except Exception as err:
            conn.close()
            raise err
        start_time += time_interval
    for _ in range(20):
        try:
            consur.execute(("insert into %s values ('%s', %f, %f,)" % (table, start_time, np.random.uniform(low=(- 4), high=4), np.random.uniform(low=(- 4), high=4))))
        except Exception as err:
            conn.close()
            raise err
        start_time += time_interval
    start_time = datetime.datetime(2019, 9, 1)
    time_interval = datetime.timedelta(seconds=60)
    for _ in range(200):
        try:
            consur.execute(("insert into %s values ('%s', %f, %f,)" % (table, start_time, ((0.1 * np.random.randn(1)) - 2), ((0.1 * np.random.randn(1)) - 2))))
        except Exception as err:
            conn.close()
            raise err
        start_time += time_interval
    for _ in range(200):
        try:
            consur.execute(("insert into %s values ('%s', %f, %f,)" % (table, start_time, ((0.1 * np.random.randn(1)) + 2), ((0.1 * np.random.randn(1)) + 2))))
        except Exception as err:
            conn.close()
            raise err
        start_time += time_interval
    for _ in range(20):
        try:
            consur.execute(("insert into %s values ('%s', %f, %f,)" % (table, start_time, np.random.uniform(low=(- 4), high=4), np.random.uniform(low=(- 4), high=4))))
        except Exception as err:
            conn.close()
            raise err
        start_time += time_interval
    if ground_truth_flag:
        n_outliers = 20
        ground_truth = np.ones(840, dtype=int)
        ground_truth[(- n_outliers):] = (- 1)
        ground_truth[400:420] = (- 1)
        return ground_truth
    else:
        pass
