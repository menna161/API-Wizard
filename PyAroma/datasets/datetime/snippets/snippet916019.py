from __future__ import print_function
from google.cloud import datastore
from WorkPool import WorkPool
from PriceCrawlingJob import PriceCrawlingJob
import datetime
import getopt
import json
import os
import sys
import time
import urllib2


def fetch_data(entities, datestr=None):
    tick_start = time.time()
    if (datestr == None):
        today = datetime.date.today()
        datestr = ('%04d%02d%02d' % (today.year, today.month, today.day))
    url = ('https://www.twse.com.tw/exchangeReport/MI_INDEX?response=json&date=%s&type=ALLBUT0999&_=%d' % (datestr, int((time.time() * 1000))))
    if g_verbose:
        print(('Info: fetch_data(): Fetch data from URL ... ' + url))
    rawjson = urllib2.urlopen(url).read()
    if g_verbose:
        print('Info: fetch_data(): Parsing fetched data...')
    datasheet = json.loads(rawjson)
    if ('data9' not in datasheet):
        print('Warning: No stock data fetched. Either not in a working day or unexpected format changes.')
    stocks = {}
    for stock in datasheet['data9']:
        sdata = {}
        sdata['id'] = stock[0]
        try:
            sdata['price'] = float(stock[8])
        except Exception as e:
            sdata['price'] = 0.0
        stocks[sdata['id']] = sdata
    result = {}
    for e in entities.itervalues():
        if (e['id'] not in stocks):
            if g_verbose:
                print(('Warning: Stock %s does not exist in fetched datasheet.' % e['id']))
        else:
            result[e['id']] = stocks[e['id']]
    if g_verbose:
        print(('Info: fetch_data() costs %f seconds' % (time.time() - tick_start)))
    return result
