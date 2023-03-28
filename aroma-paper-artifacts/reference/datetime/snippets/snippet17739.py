import itertools
import concurrent.futures
import sys
import json
import datetime
import traceback
import argparse
from threading import Lock, Semaphore
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
