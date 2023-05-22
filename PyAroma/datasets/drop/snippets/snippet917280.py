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


def _get_dataframe_datatypes(dataframe: pd.DataFrame, partitions=[], use_parts=False) -> dict:
    ' Gets the dtypes of the columns in the dataframe\n\n    Args:\n        dataframe (pd.DataFrame): Dataframe that has been published\n        partitions (list, Optional): List of partition columns\n        use_parts (bool, Optional): bool to determine if only partition datatypes\n            should be returned\n\n    Returns:\n        Dictionary of the column names as keys and dtypes as values,\n            if use_parts is true then only limited to partition columns\n    '
    types = dict()
    if use_parts:
        columns = partitions
    else:
        columns = dataframe.drop(labels=partitions, axis='columns').columns
    for col in columns:
        type_string = dataframe[col].dtype.name
        types[col] = type_string
    return types
