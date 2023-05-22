import ast
import boto3
from collections import OrderedDict
import datetime
from distutils.util import strtobool
import logging
import operator
from typing import Dict, List, Any
import multiprocessing as mp
from multiprocessing import get_context
import s3fs
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from .s3_naming_helper import S3NamingHelper


def convert_type(val: Any, dtype: str) -> Any:
    ' Converts the given value to the given datatype\n\n    Args:\n        val (Any): The value to convert\n        dtype (str): The type to attempt to convert to\n\n    Returns:\n        The value parsed into the new dtype\n    '
    if ((dtype == 'string') or (dtype == 'str')):
        return str(val)
    elif ((dtype == 'integer') or (dtype == 'int')):
        return int(val)
    elif (dtype == 'float'):
        return float(val)
    elif (dtype == 'datetime'):
        return datetime.datetime.strptime(val, '%Y-%m-%d %H:%M:%S')
    elif (dtype == 'category'):
        return pd.Category(val)
    elif ((dtype == 'bool') or (dtype == 'boolean')):
        return bool(strtobool(val))
