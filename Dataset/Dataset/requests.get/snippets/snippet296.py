import threading
import time
import math
import sys
import pdb
import requests
import urllib.parse
from utils.common import *
import config_utils as cf
import json
from collections import OrderedDict
import argparse
import numpy as np
import aggregate_server_json


def run(self):
    print((('Starting ' + self.url) + self.param))
    escaped_url = (self.url + self.param.replace('#', '-'))
    print('ESCAPED:', escaped_url)
    out = requests.get(escaped_url)
    try:
        self.results = json.loads(out.text, object_pairs_hook=OrderedDict)
    except:
        print('Empty response from server for input:', self.param)
        self.results = json.loads('{}', object_pairs_hook=OrderedDict)
    self.results['server'] = self.desc
    print((('Exiting ' + self.url) + self.param))
