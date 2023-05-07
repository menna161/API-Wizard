import os
import gzip
import re
import json
from collections import defaultdict, OrderedDict
import heapq
import pprint
from bisect import bisect_left
from datetime import datetime, date, timedelta
from enum import Enum
import pygraphviz as pgv
from tools.graph_analyser.graph_utils import strictify, get_score, add_backwards_edges


@staticmethod
def dict_import(data):
    'Returns a Device object created from the dictionary passed'
    device = Device(data['device_id'])
    device.records = data['records']
    device.release_first_seen = data['release_first_seen']
    for (release, sdate) in device.release_first_seen.items():
        date = datetime.strptime(sdate, '%Y-%m-%d').date()
        device.release_first_seen[release] = date
        if ((release not in Device.global_release_first_seen) or (Device.global_release_first_seen[release] > date)):
            Device.global_release_first_seen[release] = date
    device.min_date = datetime.strptime(data['min_date'], '%Y-%m-%d').date()
    device.max_date = datetime.strptime(data['max_date'], '%Y-%m-%d').date()
    return device
