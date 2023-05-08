import traceback
from urllib.request import urlopen
import json
from time import sleep
import geomath
import math
from datetime import datetime
from configparser import ConfigParser
import os


def refresh(self):
    try:
        self.req = urlopen(self.data_url)
        self.raw_data = self.req.read()
        self.json_data = json.loads(self.raw_data.decode())
        self.time = datetime.fromtimestamp(self.parser.time(self.json_data))
        self.aircraft = self.parser.aircraft_data(self.json_data, self.time)
    except Exception:
        print('exception in FlightData.refresh():')
        traceback.print_exc()
