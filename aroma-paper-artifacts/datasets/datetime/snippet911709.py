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


def hook_preconvert_stats():
    set_latex_value('NumVulnerabilities', len(vulnerabilities))
    num_vuln_all_android = 0
    num_vuln_specific = 0
    first_submission = None
    last_submission = None
    first_date = None
    last_date = None
    for vuln in vulnerabilities:
        manufacturers = vuln.manufacturers()
        if ('all' in [x[0] for x in manufacturers]):
            num_vuln_all_android += 1
        else:
            num_vuln_specific += 1
        for submission in vuln.submissions():
            on = submission.on
            if (first_submission == None):
                first_submission = on
                last_submission = on
            elif (on < first_submission):
                first_submission = on
            elif (on > last_submission):
                last_submission = on
        first = vuln.first_date()
        last = vuln.last_date()
        if (first_date == None):
            first_date = first
            last_date = last
        else:
            if (first < first_date):
                first_date = first
            if (last > last_date):
                last_date = last
    set_latex_value('NumVulnAllAndroid', num_vuln_all_android)
    set_latex_value('NumVulnSpecific', num_vuln_specific)
    set_latex_value('StartDate', first_submission)
    set_latex_value('EndDate', last_submission)
    set_latex_value('FirstDataDate', first_date)
    set_latex_value('LastDataDate', last_date)
    set_latex_value('VulnsPerYear', ((ufloat(len(vulnerabilities), sqrt(len(vulnerabilities))) / ((last_date - first_date) / datetime.timedelta(1))) * 365))
    set_latex_value('VulnsPerYearAllAndroid', ((ufloat(num_vuln_all_android, sqrt(num_vuln_all_android)) / ((last_date - first_date) / datetime.timedelta(1))) * 365))
    set_latex_value('VulnsPerYearTwosf', ((ufloat(len(vulnerabilities), sqrt(len(vulnerabilities))) / ((last_date - first_date) / datetime.timedelta(1))) * 365), sig_figs=2)
    set_latex_value('VulnsPerYearAllAndroidTwosf', ((ufloat(num_vuln_all_android, sqrt(num_vuln_all_android)) / ((last_date - first_date) / datetime.timedelta(1))) * 365), sig_figs=2)
    do_device_analyzer_analysis = False
    if do_device_analyzer_analysis:
        testdates = []
        for year in range(2011, 2019):
            for month in range(1, 13):
                testdates.append(datetime.date(year, month, 1))
        print('Analysing vulnerabilities')
        all_vulnerabilities = vulnerabilities.copy()
        for vset in hidden_vulnerabilities.values():
            all_vulnerabilities += vset
        analysis = analyse_vulnerability_exploits(all_vulnerabilities, testdates, string_keys=True)
        with open('data/exploitable_devices.json', 'w') as f:
            json.dump(analysis, f, indent=2)
        del analysis
        print('Stratified vulnerability analysis')
        stratified_analysis = analyse_vulnerability_exploits(all_vulnerabilities, testdates, string_keys=True, stratified=True)
        with open('data/exploitable_devices_stratified.json', 'w') as f:
            json.dump(stratified_analysis, f, indent=2)
        del stratified_analysis
    pool = mp.Pool(4)
    month_graphs(months_range(first_date, datetime.date.today()))
    for (version, date) in release_dates.items():
        daterange = months_range(date, datetime.date.today())
        pool.apply_async(month_graphs, args=(daterange, version))
    pool.close()
    pool.join()
