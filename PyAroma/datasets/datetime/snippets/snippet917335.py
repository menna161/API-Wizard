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


def setup_partitioned_parquet(self):
    bucket_name = self.random_name()
    t = tempfile.mkdtemp()
    self.tmpdir = t
    self._s3_bucket = bucket_name
    s3_client = boto3.client('s3')
    df = self._dataframe
    s3_client.create_bucket(Bucket=bucket_name)
    table = pa.Table.from_pandas(df)
    pq.write_to_dataset(table, root_path=str(t), partition_cols=['string_col', 'int_col', 'float_col', 'bool_col', 'datetime_col'])
    extra_args = {'partition_data_types': str(self._partition_metadata)}
    for (subdir, dirs, files) in os.walk(str(t)):
        for file in files:
            full_path = os.path.join(subdir, file)
            keysub = subdir.split(os.path.sep)[(subdir.split(os.path.sep).index('tmp') + 1):]
            self._dataset = keysub[0]
            keysub.append(file)
            key = '/'.join(keysub)
            with open(full_path, 'rb') as data:
                s3_client.upload_fileobj(data, Bucket=bucket_name, Key=key, ExtraArgs={'Metadata': extra_args})
                self._paths.append(key)
    return self._s3_bucket
