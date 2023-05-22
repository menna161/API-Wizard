import argparse
import csv
from dataclasses import asdict
import datetime
from pathlib import Path
import sys
from time import sleep
import requests
from aranet4 import client


def post_data(url, current):
    now = datetime.datetime.now(datetime.timezone.utc).replace(microsecond=0)
    delta_ago = datetime.timedelta(seconds=current.ago)
    t = (now - delta_ago)
    t = t.replace(second=0)
    data = {'time': t.timestamp(), 'co2': current.co2, 'temperature': current.temperature, 'pressure': current.pressure, 'humidity': current.humidity, 'battery': current.battery}
    r = requests.post(url, data=data)
    print('Pushing data: {:s}'.format(r.text))
