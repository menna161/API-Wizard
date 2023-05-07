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


def parse_line(line):
    'Get the date and information from a log file line'
    line = line.strip('\n')
    items = line.split(';')
    if (items[2] == '(invalid date)'):
        date = None
    else:
        date = datetime.strptime(items[2], '%Y-%m-%dT%H:%M:%S.%f%z').date()
    data = items[4]
    return (date, data)
