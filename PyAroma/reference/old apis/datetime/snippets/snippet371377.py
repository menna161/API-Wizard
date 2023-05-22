import hashlib
import os
import json
import datetime
import calendar
import time


def write_timestamp(at_hash):
    filename = get_timestamp_filename()
    try:
        f = open(filename, 'r')
        timestamps = json.load(f)
        f.close()
    except Exception:
        timestamps = {}
    timestamps[at_hash] = int(datetime.datetime.timestamp(datetime.datetime.now()))
    f = open(filename, 'w')
    json.dump(timestamps, f)
