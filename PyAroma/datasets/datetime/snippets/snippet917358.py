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


def test_get_data_types_from_s3():
    with get_s3_client() as s3_client:
        (bucket, parquet_paths) = setup_partitioned_parquet(s3_client=s3_client)
        s3_client = boto3.client('s3')
        files = s3_client.list_objects_v2(Bucket=bucket)
        first_file_key = files['Contents'][0]['Key']
        partition_metadata = fetch_parq._get_partitions_and_types(first_file_key, bucket)
        assert (partition_metadata == {'string_col': 'string', 'int_col': 'integer', 'float_col': 'float', 'bool_col': 'boolean', 'datetime_col': 'datetime'})
