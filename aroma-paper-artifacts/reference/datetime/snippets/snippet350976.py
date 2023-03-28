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


def display_logs(self, query: str, start: datetime, end: datetime, limit: int=1000, cli: bool=True):
    logs = list_logs(self, query, start, end, limit)
    if cli:
        for log in logs:
            print(json.dumps(log))
    else:
        sent_log = []
        for log in logs:
            if ('body' in log['content']['attributes']):
                if ('errors' in log['content']['attributes']['body']):
                    log['content']['attributes']['body']['errors'] = ''
            sent_log.append(log['content'])
        return sent_log
