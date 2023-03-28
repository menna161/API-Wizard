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


def datetime_to_str(d: datetime) -> str:
    if (d.tzinfo is None):
        d = d.replace(tzinfo=timezone.utc)
    return d.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
