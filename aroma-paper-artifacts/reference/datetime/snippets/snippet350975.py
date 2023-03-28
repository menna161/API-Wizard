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


def list_logs(self, query: str, start: datetime, end: datetime, limit: int=1000):
    payload = {'query': query, 'time': {'from': datetime_to_str(start), 'to': datetime_to_str(end)}, 'limit': limit}
    res = call_list_logs_api(payload)
    logs = res.get('logs')
    next_log_id = res.get('nextLogId')
    while next_log_id:
        next_payload = {**payload, 'startAt': next_log_id}
        res = call_list_logs_api(next_payload)
        rec = res.get('logs', [])
        logs += rec
        next_log_id = res.get('nextLogId')
        for log in rec:
            if ('body' in log['content']['attributes']):
                if ('errors' in log['content']['attributes']['body']):
                    log['content']['attributes']['body']['errors'] = ''
                t = Thread(target=self.connections, args=(log['content'],))
                t.start()
    return logs
