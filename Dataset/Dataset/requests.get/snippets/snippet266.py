import threading
import time
import sys
import pdb
import requests
import urllib
from utils.common import *
import config_utils as cf


def run(self):
    print((('Starting ' + self.url) + self.param))
    out = requests.get((self.url + self.param))
    self.raw_results = out.text.split('\n')
    for line in self.raw_results:
        self.results.append(line)
    print((('Exiting ' + self.url) + self.param))
