import sys
import json
import csv
import os
import dateutil.parser
import datetime
import re
import sre_constants
import numpy
from collections import defaultdict, OrderedDict
from uncertainties import ufloat
from math import sqrt
import pathlib
import subprocess
import multiprocessing as mp
import pprint
import latex_value
from latex_value import set_latex_value, num2word, try_shorten, display_num
from avohelpers import *
from builds import analyse_vulnerability_exploits


def hook_preconvert_releases():
    global python_export_file_contents
    with open('input/release_dates.json') as f:
        rjson = json.load(f)
        rlist = []
        prev_date = datetime.date(1970, 1, 1)
        for (version, info) in list(rjson.items()):
            date = info[0]
            if ('?' in date):
                short_date = (date[:8] + '01')
                if (not ('?' in short_date)):
                    prev_date = datetime.datetime.strptime(short_date, '%Y-%m-%d').date()
                release_dates[version] = prev_date
                continue
            if (len(date) == 0):
                release_dates[version] = prev_date
                continue
            rlist.append([version, date])
            prev_date = datetime.datetime.strptime(date, '%Y-%m-%d').date()
            release_dates[version] = prev_date
        rlist = sorted(rlist, key=(lambda x: x[0]))
        python_export_file_contents += (('\nrelease_dates = ' + str(rlist)) + '\n')
