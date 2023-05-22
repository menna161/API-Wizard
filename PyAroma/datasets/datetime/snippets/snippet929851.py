import datetime
import os
import sys


def get_log_created_year(input_file):
    'Get year from log file system timestamp\n    '
    log_created_time = os.path.getctime(input_file)
    log_created_year = datetime.datetime.fromtimestamp(log_created_time).year
    return log_created_year
