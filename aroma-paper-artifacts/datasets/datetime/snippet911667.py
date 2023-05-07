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


def _get_devices():
    'Load devices in from analysing Device Analyzer data'
    global _devices
    if (_devices is None):
        get_devices_from_file()
    start = len(_devices)
    if ((MAXLEN > 0) and (start > MAXLEN)):
        return _devices[:MAXLEN]
    if ((start < MAXLEN) or (MAXLEN == (- 1))):
        dumps = os.listdir(PATH)
        if (MAXLEN == (- 1)):
            dumps = dumps[start:]
        else:
            dumps = dumps[start:MAXLEN]
        for (index, dump) in enumerate(dumps):
            try:
                with gzip.open((PATH + dump), 'rt') as infile:
                    device = Device(dump)
                    content = infile.readline()
                    os_string = ''
                    os_date = datetime(1970, 1, 1).date()
                    build_string = ''
                    build_date = datetime(1970, 1, 1).date()
                    os_string_found = False
                    while content:
                        if (';system|osstring;' in content):
                            if (os_string_found and (os_date != None)):
                                device.add_record(os_date, os_string, None)
                            (os_date, os_string) = parse_line(content)
                            os_string_found = True
                        elif (';system|build|fingerprint;' in content):
                            (build_date, build_string) = parse_line(content)
                            if times_within(build_date, os_date, TIME_GAP):
                                device.add_record(build_date, os_string, build_string)
                                os_string_found = False
                        content = infile.readline()
                    pprint.pprint(device.release_first_seen)
                    _devices.append(device)
            except EOFError:
                print('Invalid file:', dump)
                continue
        if (len(dumps) > 0):
            save_devices_to_file()
    return _devices
