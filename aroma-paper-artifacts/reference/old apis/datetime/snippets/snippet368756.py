import time
from datetime import datetime, timedelta
from athena_glue_service_logs.partitioners.grouped_date_partitioner import GroupedDatePartitioner
from utils import S3Stubber


def today_objects_request():
    today = datetime.utcfromtimestamp(time.time()).date()
    return {'Bucket': 'nowhere', 'MaxKeys': 10, 'Prefix': ('us-west-2/' + today.strftime('%Y/%m/%d'))}
