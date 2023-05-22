import time
from datetime import datetime, timedelta
from athena_glue_service_logs.partitioners.grouped_date_partitioner import GroupedDatePartitioner
from utils import S3Stubber


def today_objects():
    today = datetime.utcfromtimestamp(time.time()).date()
    return [{'Key': ('/us-west-2/%s/some_data.json.gz' % today.strftime('%Y/%m/%d')), 'LastModified': datetime(2017, 1, 23), 'ETag': 'string', 'Size': 123, 'StorageClass': 'STANDARD', 'Owner': {'DisplayName': 'string', 'ID': 'string'}}]
