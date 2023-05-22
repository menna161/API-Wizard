import os
import json
import pandas
from datetime import datetime


def load_device_analyzer_data(path):
    'Load Device Analyzer Data from file'
    if (not os.path.isfile(path)):
        raise Exception('Device Analyzer data not found')
    records = dict()
    with open(path, 'r') as f:
        rjson = json.load(f)
        for (sdate, counts) in rjson.items():
            date = datetime.strptime(sdate, '%Y-%m-%d').date()
            records[date] = counts
    return records
