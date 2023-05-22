import pandas as pd
import numpy as np


def load_search_history(path_or_buf: str, timezone: str) -> pd.DataFrame:
    'Create the search dataframe from a path or a json string'
    df = pd.read_json(path_or_buf)
    df['time'] = pd.to_datetime(df['time'], infer_datetime_format=True)
    df['time'] = df['time'].map((lambda x: x.astimezone(timezone)))
    df = df[['title', 'time']]
    return df
