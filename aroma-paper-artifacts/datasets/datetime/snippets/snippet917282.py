import boto3
import s3fs
import re
import sys
import logging
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from typing import List
from s3parq.session_helper import SessionHelper
from s3parq import publish_redshift
from sqlalchemy import Column, Integer, String


def _parse_dataframe_col_types(dataframe: pd.DataFrame, partitions: list, custom_redshift_columns: dict=None) -> dict:
    ' Determines the metadata of the partition columns based on dataframe dtypes\n\n    Args:\n        dataframe (pd.DataFrame): Dataframe to parse the types of\n        partitions (list): Partitions in the dataframe to get the type of\n        custom_redshift_columns (dict, Optional):\n            This dictionary contains custom column data type definitions for redshift.\n            The params should be formatted as follows:\n                - column name (str)\n                - data type (str)\n\n    Returns:\n        Dictionary of column names as keys with their datatypes (string form) as values\n    '
    logger.debug('Determining write metadata for publish...')
    dataframe = dataframe[partitions]
    dtypes = {}
    for (col, dtype) in dataframe.dtypes.items():
        dtype = dtype.name
        if (dtype == 'object'):
            dtypes[col] = 'string'
        elif dtype.startswith('int'):
            dtypes[col] = 'integer'
        elif dtype.startswith('float'):
            dtypes[col] = 'float'
        elif dtype.startswith('date'):
            dtypes[col] = 'datetime'
        elif dtype.startswith('category'):
            dtypes[col] = 'category'
        elif (dtype == 'bool'):
            dtypes[col] = 'boolean'
        if custom_redshift_columns:
            if ('DECIMAL' in custom_redshift_columns[col]):
                dtypes[col] = 'decimal'
    logger.debug(f'Done. Metadata determined as {dtypes}')
    return dtypes
