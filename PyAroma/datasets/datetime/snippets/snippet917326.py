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


def __init__(self, count=1000000, s3=False, files=False):
    ' If s3 then will populate the s3 bucket with partitioned parquet. '
    warnings.warn('MockHelper is a mess and will be removed in s3parq version 2.20', DeprecationWarning)
    self._dataframe = self.setup_grouped_dataframe(count=count)
    self._s3_bucket = ''
    self._dataset = ''
    self._paths = []
    self._partition_metadata = {'string_col': 'string', 'int_col': 'integer', 'float_col': 'float', 'bool_col': 'boolean', 'datetime_col': 'datetime'}
    if s3:
        self._s3_bucket = self.setup_partitioned_parquet()
    if files:
        self._file_ops = self.setup_files_list(count)
