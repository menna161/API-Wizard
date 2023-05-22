import boto3
from collections import OrderedDict
import datetime
from mock import patch
import moto
import pandas as pd
import pytest
import contextlib
import s3parq.fetch_parq as fetch_parq
from s3parq.testing_helper import sorted_dfs_equal_by_pandas_testing, setup_grouped_dataframe, setup_partitioned_parquet


def test_s3_partitioned_parquet_to_dataframe():
    with get_s3_client() as s3_client:
        partition_types = {'string_col': 'string', 'int_col': 'integer', 'float_col': 'float', 'bool_col': 'boolean', 'datetime_col': 'datetime'}
        columns = dict(partition_types)
        columns['metrics'] = 'int'
        bucket = 'foobucket'
        key = 'fookey'
        df = setup_grouped_dataframe(count=10, columns=columns)
        (bucket, parquet_paths) = setup_partitioned_parquet(dataframe=df, bucket=bucket, key=key, partition_data_types=partition_types, s3_client=s3_client)
        first_published_file = parquet_paths[0]
        response = fetch_parq._s3_parquet_to_dataframe(bucket=bucket, key=first_published_file, partition_metadata=partition_types)
        assert isinstance(response, pd.DataFrame)
        for col in columns.keys():
            assert (col in response.columns)
        full_response = pd.DataFrame()
        for path in parquet_paths:
            full_response = full_response.append(fetch_parq._s3_parquet_to_dataframe(bucket=bucket, key=path, partition_metadata=partition_types))
        assert (full_response.shape == df.shape)
        sorted_dfs_equal_by_pandas_testing(full_response, df)
