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


def dd_last(last_):
    digit_ = last_[(- 1):]
    if (digit_ == 'm'):
        now = datetime.now()
        return (now - timedelta(minutes=int(last_.replace(digit_, ''))))
    if (digit_ == 'h'):
        now = datetime.now()
        return (now - timedelta(hours=int(last_.replace(digit_, ''))))
    if (digit_ == 'd'):
        now = datetime.now()
        return (now - timedelta(days=int(last_.replace(digit_, ''))))
    else:
        exit('You need to use a valid period: m = Minutes, h = Hours, d = Days ')
