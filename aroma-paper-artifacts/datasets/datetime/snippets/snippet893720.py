import pandas as pd
import time


@profile
def read():
    d = pd.read_csv('pandas100000.csv')
    d['ts'] = pd.to_datetime(d['ts'])
    d = d.set_index(d['ts'])
    _ = d.iloc[200:500]
