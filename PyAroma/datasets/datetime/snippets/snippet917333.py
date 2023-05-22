import os
import pytest
import boto3
from moto import mock_s3
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from dfmock import DFMock
from string import ascii_lowercase
import random
import tempfile
import warnings


def setup_grouped_dataframe(self, count):
    df = DFMock()
    df.count = count
    df.columns = {'string_col': {'option_count': 3, 'option_type': 'string'}, 'int_col': {'option_count': 3, 'option_type': 'int'}, 'float_col': {'option_count': 3, 'option_type': 'float'}, 'bool_col': {'option_count': 3, 'option_type': 'bool'}, 'datetime_col': {'option_count': 3, 'option_type': 'datetime'}, 'metrics': 'int'}
    df.generate_dataframe()
    return df.dataframe
