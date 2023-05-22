import random
import statistics
from datetime import datetime


def _get_start_and_end_ctimes(self, time_series_sorted):
    'Get the start and end times of a sorted time series data as ctime. '
    start_timestamp = time_series_sorted[0][0]
    end_timestamp = time_series_sorted[(- 1)][0]
    start_ctime = datetime.fromtimestamp(float(start_timestamp)).ctime()
    end_ctime = datetime.fromtimestamp(float(end_timestamp)).ctime()
    return (start_ctime, end_ctime)
