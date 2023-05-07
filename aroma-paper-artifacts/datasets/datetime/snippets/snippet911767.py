import datetime
import json
import os
import re
import pygraphviz as pgv


def load_version_dates(path):
    'Load the release dates of Android versions from the path given'
    output = dict()
    if os.path.isfile(path):
        with open(path, 'r') as f:
            rjson = json.load(f)
            for (version, sdateref) in rjson.items():
                sdate = sdateref[0]
                if (len(sdate) == 0):
                    continue
                if (('?' in sdate) or (len(sdate) == 0)):
                    if ('?' in sdate[:8]):
                        continue
                    sdate = (sdate[:8] + '01')
                output[version] = datetime.datetime.strptime(sdate, '%Y-%m-%d').date()
    return output
