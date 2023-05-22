import os
import time
from datetime import datetime
import boto3
from botocore.exceptions import ClientError


def format_datetime_object(datetime_object, date_time_format):
    'Get Formatted Datetime Object Routine'
    return datetime.strptime(datetime_object.strftime(date_time_format), date_time_format)
