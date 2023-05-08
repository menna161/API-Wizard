import concurrent.futures
import itertools
import json
import datetime
import traceback
import sys
import argparse
import base64
import time
from collections import namedtuple
from http.server import BaseHTTPRequestHandler, HTTPServer
from random import choice, randint
from string import ascii_letters
from threading import Thread
import requests


def error(message, **kwargs):
    print('[{}] {}'.format(datetime.datetime.now().time(), message), sys.stderr)
    for (n, a) in kwargs.items():
        print('\t{}={}'.format(n, a), sys.stderr)
    (exc_type, exc_value, exc_traceback) = sys.exc_info()
    print(('Exception type:' + str(exc_type)), sys.stderr)
    print(('Exception value:' + str(exc_value)), sys.stderr)
    print('TRACE:', sys.stderr)
    traceback.print_tb(exc_traceback, file=sys.stderr)
    print('\n\n\n', sys.stderr)
