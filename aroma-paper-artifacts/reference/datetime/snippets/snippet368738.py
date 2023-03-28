import time
from datetime import datetime, timedelta
from athena_glue_service_logs.partitioners.date_partitioner import DatePartitioner
from utils import S3Stubber


def basic_s3_key():
    return {'Key': '/2017/08/11/some_data.json.gz', 'LastModified': datetime(2017, 1, 23), 'ETag': 'string', 'Size': 123, 'StorageClass': 'STANDARD', 'Owner': {'DisplayName': 'string', 'ID': 'string'}}
