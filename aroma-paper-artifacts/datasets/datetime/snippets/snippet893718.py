import numpy as np
import datetime
import taos
import time


def insert_demo_data(conn, consur, database, table):
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
        consur.execute(('create table if not exists %s (ts timestamp, a float, b float, d float, e float, f float)' % table))
    except Exception as err:
        conn.close()
        raise err
    start_time = datetime.datetime(2018, 8, 1)
    time_interval = datetime.timedelta(seconds=60)
    current_time = time.clock()
    for _ in range(100000):
        try:
            consur.execute(("insert into %s values ('%s', %f, %f,%f,%f,%f)" % (table, start_time, np.random.uniform(low=(- 4), high=4), np.random.uniform(low=(- 4), high=4), np.random.uniform(low=(- 4), high=4), np.random.uniform(low=(- 4), high=4), np.random.uniform(low=(- 4), high=4))))
        except Exception as err:
            conn.close()
            raise err
        start_time += time_interval
    print(('Total inserting cost: %.6f s' % (time.clock() - current_time)))
