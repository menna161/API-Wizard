import time
from datetime import datetime, timedelta
from athena_glue_service_logs.partitioners.date_partitioner import DatePartitioner
from utils import S3Stubber


def today():
    return datetime.utcfromtimestamp(time.time()).date()
