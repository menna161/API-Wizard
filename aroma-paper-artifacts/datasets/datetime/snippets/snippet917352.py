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


@pytest.mark.slow
def test_fetches_nons3parq_large_parquet():
    input_key = 'burger-shipment/buns'
    input_bucket = 'loadingdock'
    df = dfmock.DFMock(count=100000)
    df.columns = {'string_options': {'option_count': 4, 'option_type': 'string'}, 'int_options': {'option_count': 4, 'option_type': 'int'}, 'datetime_options': {'option_count': 5, 'option_type': 'datetime'}, 'float_options': {'option_count': 2, 'option_type': 'float'}, 'metrics': 'integer'}
    df.generate_dataframe()
    df.grow_dataframe_to_size(500)
    input_df = pd.DataFrame(df.dataframe)
    s3_client = boto3.client('s3')
    s3_key = 'burger-shipment/buns'
    setup_nons3parq_parquet(dataframe=input_df, bucket=input_bucket, key=input_key, s3_client=s3_client)
    fetched_diff = fetch_parq.fetch(bucket=input_bucket, key=s3_key, parallel=False)
    assert (fetched_diff.shape == input_df.shape)
    sorted_dfs_equal_by_pandas_testing(fetched_diff, input_df)
