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


def parse_datetime_str(s: str) -> datetime:
    return datetime.strptime(s, DATETIME_FORMAT)
