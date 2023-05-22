import boto3
from contextlib import ExitStack
from dfmock import DFMock
import logging
import moto
import os
import pandas as pd
import numpy as np
from pandas.util.testing import assert_frame_equal
import pyarrow as pa
import pyarrow.parquet as pq
import random
from string import ascii_lowercase
import tempfile
from typing import Dict


def setup_grouped_dataframe(count: int=100, columns: Dict=None):
    ' Creates mock dataframe using dfmock\n\n    Args:\n        count (int): Row length to generate on the dataframe\n        columns (Dict): dictionary of columns and types, following dfmock guides\n\n    Returns:\n        A freshly mocked dataframe\n    '
    df = DFMock()
    df.count = count
    if (not columns):
        columns = {'string_col': {'option_count': 3, 'option_type': 'string'}, 'int_col': {'option_count': 3, 'option_type': 'int'}, 'float_col': {'option_count': 3, 'option_type': 'float'}, 'bool_col': {'option_count': 3, 'option_type': 'bool'}, 'datetime_col': {'option_count': 3, 'option_type': 'datetime'}, 'text_col': 'string', 'metrics': 'int'}
    df.columns = columns
    df.generate_dataframe()
    return df.dataframe
