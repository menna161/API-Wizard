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


def query_data(conn, cursor, database, table, start_time, end_time, time_serie_name, ground_truth=None, time_serie=False, ground_truth_flag=True):
    '\n    Query data from given time range and table.\n\n    Parameters\n    ----------\n    conn: taos.connection.TDengineConnection\n        TDEnginine connection name.\n    cursor: taos.cursor.TDengineCursor\n        TDEnginine cursor name.\n    database: str\n        Connect database name.\n    table: str\n        Table to query from.\n    start_time: str\n        Time range, start from.\n    end_time: str\n        Time range, end from.\n    time_serie_name: str\n        Time_serie column name in the table.\n    ground_truth: numpy array of shape (n_samples,), optional (default=None)\n        Ground truth value, for evaluation and visualization.\n    time_serie: bool, optional (default=False)\n        Whether contains time stamps as one of the features or not.\n    ground_truth_flag: bool, optional (default=False)\n        Whether uses ground truth to evaluate the performance or not.\n\n    Returns\n    -------\n    X: pandas DataFrame\n        Queried data as DataFrame from given table and time range.\n\n    '
    if (start_time and end_time):
        try:
            cursor.execute(("select * from %s.%s where %s >= '%s' and %s <= '%s' " % (database, table, time_serie_name, start_time, time_serie_name, end_time)))
        except Exception as err:
            conn.close()
            raise err
    elif ((not start_time) and (not end_time)):
        try:
            cursor.execute(('select * from %s.%s' % (database, table)))
        except Exception as err:
            conn.close()
            raise err
    elif (start_time and (not end_time)):
        try:
            cursor.execute(("select * from %s.%s where %s >=  '%s' " % (database, table, time_serie_name, start_time)))
        except Exception as err:
            conn.close()
            raise err
    elif ((not start_time) and end_time):
        try:
            cursor.execute(("select * from %s.%s where %s <=  '%s' " % (database, table, time_serie_name, end_time)))
        except Exception as err:
            conn.close()
            raise err
    cols = cursor.description
    data = cursor.fetchall()
    if (start_time and end_time):
        try:
            cursor.execute(("select * from %s.%s where %s >=  '%s' and %s <=  '%s' " % (database, table, time_serie_name, start_time, time_serie_name, end_time)))
        except Exception as err:
            conn.close()
            raise err
    elif ((not start_time) and (not end_time)):
        try:
            cursor.execute(('select * from %s.%s' % (database, table)))
        except Exception as err:
            conn.close()
            raise err
    elif (start_time and (not end_time)):
        try:
            cursor.execute(("select * from %s.%s where %s >=  '%s' " % (database, table, time_serie_name, start_time)))
        except Exception as err:
            conn.close()
            raise err
    elif ((not start_time) and end_time):
        try:
            cursor.execute(("select * from %s.%s where %s <=  '%s' " % (database, table, time_serie_name, end_time)))
        except Exception as err:
            conn.close()
            raise err
    tmp = pd.DataFrame(list(data))
    if time_serie:
        X = tmp
    else:
        X = tmp.iloc[(:, 1:)]
    if ground_truth_flag:
        if True:
            try:
                cursor.execute(('select * from %s.%s' % (database, table)))
            except Exception as err:
                conn.close()
                raise err
            whole_data = cursor.fetchall()
            try:
                cursor.execute(('select * from %s.%s' % (database, table)))
            except Exception as err:
                conn.close()
                raise err
            whole_tmp = pd.DataFrame(list(whole_data))
            timestamp = np.array(whole_tmp.iloc[(:, 0)].to_numpy(), dtype='datetime64')
            timestamp = np.reshape(timestamp, (- 1))
            new_ground_truth = []
            if (start_time and end_time):
                for i in range(len(whole_tmp)):
                    if ((timestamp[i] >= np.datetime64(start_time)) and (timestamp[i] <= np.datetime64(end_time))):
                        new_ground_truth.append(ground_truth[i])
            elif (start_time and (not end_time)):
                for i in range(len(whole_tmp)):
                    if (timestamp[i] >= np.datetime64(start_time)):
                        new_ground_truth.append(ground_truth[i])
            elif ((not start_time) and end_time):
                for i in range(len(whole_tmp)):
                    if (timestamp[i] <= np.datetime64(end_time)):
                        new_ground_truth.append(ground_truth[i])
            elif ((not start_time) and (not end_time)):
                new_ground_truth = ground_truth
            new_ground_truth = np.array(new_ground_truth)
        else:
            new_ground_truth = ground_truth
        X.fillna(method='ffill')
        X.fillna(method='bfill')
        return (X, new_ground_truth)
    else:
        X.fillna(method='ffill')
        X.fillna(method='bfill')
        return X
