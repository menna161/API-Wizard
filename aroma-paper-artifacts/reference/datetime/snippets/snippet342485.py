import argparse
import csv
from dataclasses import asdict
import datetime
from pathlib import Path
import sys
from time import sleep
import requests
from aranet4 import client


def parse_args(ctl_args):
    parser = argparse.ArgumentParser()
    parser.add_argument('device_mac', nargs='?', help='Aranet4 Bluetooth Address')
    parser.add_argument('--scan', action='store_true', help='Scan Aranet4 devices')
    current = parser.add_argument_group('Options for current reading')
    current.add_argument('-u', '--url', metavar='URL', help='Remote url for current value push')
    parser.add_argument('-r', '--records', action='store_true', help='Fetch historical log records')
    history = parser.add_argument_group('Filter History Log Records')
    history.add_argument('-s', '--start', metavar='DATE', type=datetime.datetime.fromisoformat, help='Records range start (UTC time, example: 2019-09-29T14:00:00')
    history.add_argument('-e', '--end', metavar='DATE', type=datetime.datetime.fromisoformat, help='Records range end (UTC time, example: 2019-09-30T14:00:00')
    history.add_argument('-o', '--output', metavar='FILE', type=Path, help='Save records to a file')
    history.add_argument('-w', '--wait', action='store_true', default=False, help='Wait until new data point available')
    history.add_argument('-l', '--last', metavar='COUNT', type=int, help='Get <COUNT> last records')
    history.add_argument('--xt', dest='temp', default=True, action='store_false', help="Don't get temperature records")
    history.add_argument('--xh', dest='humi', default=True, action='store_false', help="Don't get humidity records")
    history.add_argument('--xp', dest='pres', default=True, action='store_false', help="Don't get pressure records")
    history.add_argument('--xc', dest='co2', default=True, action='store_false', help="Don't get co2 records")
    return parser.parse_args(ctl_args)
