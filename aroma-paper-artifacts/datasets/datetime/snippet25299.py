from lxml import etree
from datetime import datetime
import pandas as pd


def build_dataframe(self):
    '\n        Builds a pandas dataframe.\n        '
    df = pd.DataFrame.from_dict(self._data, orient='index')
    df.columns = self._header_list
    df = df.set_index(pd.to_datetime(df.index))
    df = df.astype(float)
    return df
