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


def _parquet_schema(dataframe: pd.DataFrame, custom_redshift_columns: dict=None):
    ' Translates pandas dtypes to PyArrow types and creates a Schema from them\n\n    Args:\n        dataframe (pd.DataFrame): Dataframe to pull the schema of\n        custom_redshift_columns (dict, Optional): \n            This dictionary contains custom column data type definitions for redshift.\n            The params should be formatted as follows:\n                - column name (str)\n                - data type (str)\n\n    Returns:\n        PyArrow Schema of the given dataframe\n        Potentially modified Dataframe\n    '
    fields = []
    for (col, dtype) in dataframe.dtypes.items():
        dtype = dtype.name
        if (dtype == 'object'):
            if custom_redshift_columns:
                if ('[Decimal(' in str(dataframe[col].values)[:9]):
                    s = custom_redshift_columns[col]
                    precision = int(s[(s.find('DECIMAL(') + len('DECIMAL(')):s.rfind(',')].strip())
                    scale = int(s[(s.find(',') + len(',')):s.rfind(')')].strip())
                    pa_type = pa.decimal128(precision=precision, scale=scale)
                else:
                    pa_type = pa.string()
            else:
                pa_type = pa.string()
        elif dtype.startswith('int32'):
            pa_type = pa.int32()
        elif dtype.startswith('int64'):
            pa_type = pa.int64()
        elif dtype.startswith('int8'):
            pa_type = pa.int8()
        elif dtype.startswith('Int32'):
            dataframe = dataframe.astype({col: 'object'})
            pa_type = pa.int32()
        elif dtype.startswith('Int64'):
            dataframe = dataframe.astype({col: 'object'})
            pa_type = pa.int64()
        elif dtype.startswith('float32'):
            pa_type = pa.float32()
        elif dtype.startswith('float64'):
            pa_type = pa.float64()
        elif dtype.startswith('float16'):
            pa_type = pa.float16()
        elif dtype.startswith('datetime'):
            pa_type = pa.timestamp('ns')
        elif dtype.startswith('date'):
            pa_type = pa.date64()
        elif dtype.startswith('category'):
            pa_type = pa.string()
        elif (dtype == 'bool'):
            pa_type = pa.bool_()
        else:
            raise NotImplementedError(f'Error: {dtype} is not a datatype which can be mapped to Parquet using s3parq.')
        fields.append(pa.field(col, pa_type))
    return (pa.schema(fields=fields), dataframe)
