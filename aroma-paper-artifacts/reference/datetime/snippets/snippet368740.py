import time
from datetime import datetime, timedelta
from athena_glue_service_logs.partitioners.date_partitioner import DatePartitioner
from utils import S3Stubber


def today_objects():
    return [{'Key': ('/%s/some_data.json.gz' % today().strftime('%Y/%m/%d')), 'LastModified': datetime(2017, 1, 23), 'ETag': 'string', 'Size': 123, 'StorageClass': 'STANDARD', 'Owner': {'DisplayName': 'string', 'ID': 'string'}}, {'Key': ('/%s/more_data.json.gz' % today().strftime('%Y/%m/%d')), 'LastModified': datetime(2017, 1, 23), 'ETag': 'string', 'Size': 123, 'StorageClass': 'STANDARD', 'Owner': {'DisplayName': 'string', 'ID': 'string'}}]
