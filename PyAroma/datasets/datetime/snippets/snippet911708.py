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


def months_range(start_date, end_date, day_of_month=1):
    'Return a list of dates over the period from start_date to end_date, on day_of_month of each month in this period'
    day = start_date.day
    month = start_date.month
    year = start_date.year
    if (day > day_of_month):
        day = day_of_month
        month += 1
    elif (day < day_of_month):
        day = day_of_month
    dates = []
    while True:
        if (month == 13):
            month = 1
            year += 1
        to_add = datetime.date(year, month, day)
        if (to_add > end_date):
            break
        dates.append(to_add)
        month += 1
    return dates
