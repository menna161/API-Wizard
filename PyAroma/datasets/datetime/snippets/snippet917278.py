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


def _gen_parquet_to_s3(bucket: str, key: str, dataframe: pd.DataFrame, partitions: list, custom_redshift_columns: dict=None) -> None:
    " Converts the dataframe into a PyArrow table then writes it into S3 as\n    parquet. Partitions are done with PyArrow parquet's write.\n    NOTE: Timestamps are coerced to ms , this is due to a constraint of parquet\n        with pandas's datetime64\n\n    Args:\n        bucket (str): S3 bucket to publish to\n        key (str): S3 key to the root of where the dataset should be published\n        dataframe (pd.DataFrame): Dataframe that's being published\n        partitions (list): List of partition columns\n        custom_redshift_columns (dict): \n            This dictionary contains custom column data type definitions for redshift.\n            The params should be formatted as follows:\n                - column name (str)\n                - data type (str)\n\n    Returns:\n        None\n    "
    logger.info('Writing to S3...')
    try:
        (schema, frame) = _parquet_schema(dataframe, custom_redshift_columns=custom_redshift_columns)
        table = pa.Table.from_pandas(df=frame, schema=schema, preserve_index=False)
    except pa.lib.ArrowTypeError:
        logger.warning('Dataframe conversion to pyarrow table failed, checking object columns for mixed types')
        dataframe_dtypes = dataframe.dtypes.to_dict()
        object_columns = [col for (col, col_type) in dataframe_dtypes.items() if ((col_type == 'object') and ('[Decimal(' not in str(dataframe[col].values)[:9]))]
        for object_col in object_columns:
            if (not dataframe[object_col].apply(isinstance, args=[str]).all()):
                logger.warning(f'Dataframe column : {object_col} : in this chunk is type object but contains non-strings, converting to all-string column')
                dataframe[object_col] = dataframe[object_col].astype(str)
        logger.info('Retrying conversion to pyarrow table')
        (schema, frame) = _parquet_schema(dataframe, custom_redshift_columns=custom_redshift_columns)
        table = pa.Table.from_pandas(df=frame, schema=schema, preserve_index=False)
    uri = s3_url(bucket, key)
    logger.debug(f'Writing to s3 location: {uri}...')
    pq.write_to_dataset(table, compression='snappy', root_path=uri, partition_cols=partitions, filesystem=s3fs.S3FileSystem(), coerce_timestamps='ms', allow_truncated_timestamps=True)
    logger.debug('Done writing to location.')
