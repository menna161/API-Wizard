from pprint import pprint
import os, yaml, json, sys, argparse, logging, re, datetime
import pynetbox
from netaddr import *


def modification_date(filename):
    t = os.path.getmtime(filename)
    return datetime.datetime.fromtimestamp(t)
