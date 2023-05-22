import pdb
import requests
import sys
import urllib.parse
import numpy as np
from collections import OrderedDict
import argparse
import config_utils as cf


def dispatch_request(self, url):
    max_retries = 10
    attempts = 0
    while True:
        try:
            r = requests.get(url, timeout=1000)
            if (r.status_code == 200):
                return r
        except:
            print('Request:', url, ' failed. Retrying...')
        attempts += 1
        if (attempts >= max_retries):
            print('Request:', url, ' failed')
            break
