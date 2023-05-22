import sys
import glob
from datetime import datetime, timedelta
import traces
from traces.utils import datetime_range


def parse_iso_datetime(value):
    return datetime.strptime(value, '%Y-%m-%dT%H:%M:%S')
