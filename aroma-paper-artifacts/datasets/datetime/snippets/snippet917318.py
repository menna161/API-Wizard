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


def setup_partitioned_parquet(dataframe: pd.DataFrame=None, bucket: str=None, key: str=None, partition_data_types: Dict=None, s3_client=None):
    ' Creates temporary files and publishes them to the mocked S3 to test fetches,\n    will fill in unsupplied parameters with random values or defaults\n\n    Args:\n        dataframe (pd.DataFrame): dataframe to split into parquet files\n        bucket (str, Optional): bucket to create to put parquet files in,\n            will be a random string if not supplied\n        key (str, Optional): S3 key to put parquet files in, will be a random\n            string if not supplied\n        partition_data_types (Dict, Optional): partition columns and datatypes,\n            will be the default if not supplied\n        s3_client (boto3 S3 client, Optional): The started S3 client that boto\n            uses - NOTE: this should be made under a moto S3 mock!\n            If it is not provided, a session is crafted under moto.mock_s3\n\n    Returns:\n        A tuple of the bucket and the published parquet file paths\n    '
    if (dataframe is None):
        dataframe = setup_grouped_dataframe()
    if (not key):
        key = setup_random_string()
    if (not bucket):
        bucket = setup_random_string()
    if (partition_data_types is None):
        partition_data_types = {'string_col': 'string', 'int_col': 'integer', 'float_col': 'float', 'bool_col': 'boolean', 'datetime_col': 'datetime'}
    with ExitStack() as stack:
        tmp_dir = stack.enter_context(tempfile.TemporaryDirectory())
        s3_client.create_bucket(Bucket=bucket)
        table = pa.Table.from_pandas(dataframe)
        pq.write_to_dataset(table, root_path=str(tmp_dir), partition_cols=list(partition_data_types.keys()))
        parquet_paths = []
        extra_args = {'partition_data_types': str(partition_data_types)}
        for (subdir, dirs, files) in os.walk(str(tmp_dir)):
            for file in files:
                full_path = os.path.join(subdir, file)
                full_key = '/'.join([key, subdir.replace(f'{tmp_dir}/', ''), file])
                with open(full_path, 'rb') as data:
                    s3_client.upload_fileobj(data, Bucket=bucket, Key=full_key, ExtraArgs={'Metadata': extra_args})
                    parquet_paths.append(full_key)
    return (bucket, parquet_paths)
