import boto3
import datetime
import dfmock
from mock import patch
import moto
import pandas as pd
import pytest
import random
import contextlib
import s3parq.fetch_parq as fetch_parq
from s3parq.fetch_parq import MissingS3ParqMetadata
from s3parq.testing_helper import sorted_dfs_equal_by_pandas_testing, setup_files_list, setup_grouped_dataframe, setup_nons3parq_parquet, setup_partitioned_parquet, setup_random_string


def test_get_partition_difference_datetime():
    bucket = 'safebucket'
    key = 'dataset'
    partition = 'burgertime'
    rando_values = [(datetime.datetime.now() - datetime.timedelta(seconds=random.randrange((((100 * 24) * 60) * 60)))).replace(microsecond=0) for x in range(5)]
    s3_paths = [f"{key}/{partition}={x.strftime('%Y-%m-%d %H:%M:%S')}/12345.parquet" for x in rando_values[:(- 1)]]
    with patch('s3parq.fetch_parq.get_all_files_list') as get_all_files_list:
        with patch('s3parq.fetch_parq._get_partitions_and_types') as _get_partitions_and_types:
            get_all_files_list.return_value = s3_paths
            _get_partitions_and_types.return_value = {'burgertime': 'datetime'}
            deltas = fetch_parq.get_diff_partition_values(bucket, key, partition, rando_values[:(- 2)])
            assert (deltas == [rando_values[(- 2)]])
            deltas = fetch_parq.get_diff_partition_values(bucket, key, partition, rando_values, reverse=True)
            assert (deltas == [rando_values[(- 1)]])
