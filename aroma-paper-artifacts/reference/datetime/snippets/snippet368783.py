import logging
from athena_glue_service_logs.catalog_manager import BaseCatalogManager
from athena_glue_service_logs.partitioners.date_partitioner import DatePartitioner
from athena_glue_service_logs.partitioners.grouped_date_partitioner import GroupedDatePartitioner
from awsglue.transforms import Map
from awsglue.transforms import Map
from datetime import datetime


def cast_timestamps(record):
    record['endtime'] = datetime.utcfromtimestamp(int(record['endtime'])).isoformat()
    record['starttime'] = datetime.utcfromtimestamp(int(record['starttime'])).isoformat()
    return record
