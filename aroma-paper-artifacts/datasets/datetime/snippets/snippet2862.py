import os
import json
import shutil
import urllib3
from hashlib import md5
from socket import gethostbyname
from argparse import ArgumentParser
from xml.etree import ElementTree as eTree
from datetime import datetime, timedelta
import sqlite3
import requests


def display_cache():
    '\n    Diplay cache data and exit.\n\n    :return: None\n    :rtype: None\n    '
    print('{:^30} {:^15} {:^7} {:^19} {:^32}'.format('hostname', 'ip', 'proto', 'expired', 'sessionkey'))
    print('{:-^30} {:-^15} {:-^7} {:-^19} {:-^32}'.format('-', '-', '-', '-', '-'))
    for cache in sql_cmd('SELECT * FROM skey_cache', fetch_all=True):
        (name, ip, proto, expired, sessionkey) = cache
        print('{:30} {:15} {:^7} {:19} {:32}'.format(name, ip, proto, datetime.fromtimestamp(float(expired)).strftime('%H:%M:%S %d.%m.%Y'), sessionkey))
