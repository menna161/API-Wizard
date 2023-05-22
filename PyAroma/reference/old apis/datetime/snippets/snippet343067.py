import datetime
from archon.brokerservice.brokerservice import Brokerservice
import archon.exchange.bitmex.bitmex as bitmex
import archon.exchange.exchanges as exc
import pandas as pd
import numpy
import matplotlib.pyplot as plt
from boto3 import client
import boto3
import requests
import json
import matplotlib.pyplot as plt
from numpy import array


def fetch():
    t1 = datetime.datetime.now()
    candles = bitmex_client.history_days(numdays)
    t2 = datetime.datetime.now()
    tt = (t2 - t1)
    print(('%i candles fetched in %s' % (len(candles), str(tt))))
    return candles
