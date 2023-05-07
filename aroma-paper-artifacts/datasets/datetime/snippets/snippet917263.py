import ast
import boto3
from collections import OrderedDict
import datetime
from distutils.util import strtobool
import logging
import operator
from typing import Dict, List, Any
import multiprocessing as mp
from multiprocessing import get_context
import s3fs
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
from .s3_naming_helper import S3NamingHelper


def _get_partition_value_data_types(parsed_parts: dict, part_types: dict) -> dict:
    ' Uses the partitions with their known types to parse them out\n\n    Args:\n        parsed_parts (dict): A dictionary of all partitions with their values\n        part_types (dict): A dictionary of all partitions to their datatypes\n\n    Returns:\n        A dictionary of all partitions with their values parsed into the correct datatype\n    '
    for (part, values) in parsed_parts.items():
        part_type = part_types[part]
        if ((part_type == 'string') or (part_type == 'category')):
            continue
        elif ((part_type == 'int') or (part_type == 'integer')):
            parsed_parts[part] = set(map(int, values))
        elif (part_type == 'float'):
            parsed_parts[part] = set(map(float, values))
        elif (part_type == 'datetime'):
            parsed_parts[part] = set(map((lambda s: datetime.datetime.strptime(s, '%Y-%m-%d %H:%M:%S')), values))
        elif ((part_type == 'bool') or (part_type == 'boolean')):
            parsed_parts[part] = set(map(bool, values))
        else:
            logger.debug(f'Unknown partition type : {part_type} :, leaving as a string')
    return parsed_parts
