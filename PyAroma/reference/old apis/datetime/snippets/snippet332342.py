import datetime
import os
import json
from flask import Flask
from flask import request


def get_ts():
    ts = datetime.datetime.now().isoformat()
    ts = ts.replace('-', '_')
    ts = ts.replace(':', '_')
    ts = ts.replace('.', '_')
    return ts
