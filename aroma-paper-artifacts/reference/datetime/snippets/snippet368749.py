import time
from datetime import datetime, timedelta
from athena_glue_service_logs.partitioners.grouped_date_partitioner import GroupedDatePartitioner
from utils import S3Stubber


def region_s3_keys():
    return [{'Key': 'some_logs/us-west-2/2017/08/11/some_data.json.gz', 'LastModified': datetime(2017, 1, 23), 'ETag': 'string', 'Size': 123, 'StorageClass': 'STANDARD', 'Owner': {'DisplayName': 'string', 'ID': 'string'}}, {'Key': 'some_logs/us-east-1/2018/01/09/other_data.json.gz', 'LastModified': datetime(2018, 1, 9), 'ETag': 'string', 'Size': 456, 'StorageClass': 'STANDARD', 'Owner': {'DisplayName': 'string', 'ID': 'string'}}]
