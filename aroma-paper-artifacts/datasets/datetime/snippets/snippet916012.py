from __future__ import print_function
from google.cloud import datastore
from WorkPool import WorkPool
from DividendCrawlingJob import DividendCrawlingJob
import fetch_dividend_data
import datetime
import getopt
import json
import os
import sys
import time

if (__name__ == '__main__'):
    if ('GOOGLE_APPLICATION_CREDENTIALS' not in os.environ):
        print('Error: Missing "GOOGLE_APPLICATION_CREDENTIALS" environment variable.', file=sys.stderr)
        sys.exit(1)
    try:
        (pairs, remaining) = getopt.getopt(sys.argv[1:], 'nvdy:q:hc')
    except getopt.GetoptError as e:
        print(('Error: ' + str(e)), file=sys.stderr)
        show_usage()
        sys.exit(1)
    g_verbose = False
    g_data_processing = True
    g_cdys_processing = True
    g_gdclient = datastore.Client()
    g_delete = False
    cur_date = datetime.date.today()
    g_year = cur_date.year
    if (cur_date.month <= 6):
        g_year -= 1
    for p in pairs:
        if (p[0] == '-v'):
            g_verbose = True
        elif (p[0] == '-n'):
            g_data_processing = False
        elif (p[0] == '-d'):
            g_delete = True
        elif (p[0] == '-y'):
            g_year = int(p[1])
        elif (p[0] == '-q'):
            q = g_gdclient.query(kind='tw_stock_data')
            q.add_filter('id', '=', p[1])
            for e in q.fetch():
                print(str(e))
            sys.exit(0)
        elif (p[0] == '-h'):
            show_usage()
            sys.exit(0)
        elif (p[0] == '-c'):
            g_cdys_processing = False
    if g_delete:
        b = g_gdclient.batch()
        b.begin()
        bcnt = 0
        for e in g_gdclient.query(kind='tw_stock_data').fetch():
            b.delete(e.key)
            bcnt += 1
            if (bcnt >= 500):
                b.commit()
                if g_verbose:
                    print(('Info: Deleting %d keys from database (kind = "tw_stock_data") ' % bcnt))
                b = g_gdclient.batch()
                b.begin()
                bcnt = 0
        if (bcnt > 0):
            b.commit()
            if g_verbose:
                print(('Info: Deleting %d keys from database (kind = "tw_stock_data") ' % bcnt))
        sys.exit(0)
    entities = {}
    for e in g_gdclient.query(kind='tw_stock_data').fetch():
        entities[e['id']] = e
    if g_cdys_processing:
        commit_cdys_data(entities, fetch_cdys_data(entities))
    if g_data_processing:
        years = range(g_year, (g_year - 6), (- 1))
        if g_verbose:
            print(('Info: Fetching dividend data for year range: ' + str(years)))
        data = fetch_data(years)
        commit_raw_data(entities, data)
    if (len(entities) > 0):
        if g_verbose:
            print(('Info: Computing %d entities ...' % len(entities)))
        commit_computed_data(entities)
