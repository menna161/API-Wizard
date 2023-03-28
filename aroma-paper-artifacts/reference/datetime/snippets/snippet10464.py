import time
import datetime


def get_time_str(time_diff):
    time_str = str(datetime.timedelta(seconds=time_diff))
    return time_str
