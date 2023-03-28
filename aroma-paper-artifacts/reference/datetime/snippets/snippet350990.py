import syslog_client as syslog
import re
import requests
import json
import sys
import telepot
from time import sleep
import apache_log_parser
from pygtail import Pygtail
from threading import Thread
from pyzabbix import ZabbixMetric, ZabbixSender
from datetime import datetime, timezone, timedelta
import os
from ConfigParser import ConfigParser
from configparser import ConfigParser


def run(self):
    try:
        first = True
        query = 'service:* status:warn'
        while True:
            last_2 = ''
            if first:
                now = str(datetime.now()).replace(' ', 'T').split('.')[0]
                last_2 = now
                last = str(dd_last('2m')).replace(' ', 'T').split('.')[0]
                start_datetime = parse_datetime_str(last)
                end_datetime = parse_datetime_str(now)
                print(now, last)
                display_logs(self, query, start_datetime, end_datetime, limit=1000, cli=False)
                first = False
                sleep(10)
            else:
                now = str(datetime.now()).replace(' ', 'T').split('.')[0]
                start_datetime = parse_datetime_str(last_2)
                end_datetime = parse_datetime_str(now)
                print(now, last)
                display_logs(self, query, start_datetime, end_datetime, limit=1000, cli=False)
                last_2 = now
                sleep(10)
    except Exception as e:
        print(e)
        exit()
    finally:
        sleep(0.01)
