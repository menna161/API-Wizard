from collections import defaultdict
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import pandas as pd
import random
import time
from .dataset import RESOLUTIONS


def start(self, robinhood, resolution='1d', until=None):
    'Starts live trading\n\n        Args:\n            robinhood: (Robinhood*) a robinhood client, that already has logged in\n            resolution: (str) the resolution/freq to trade at\n            until: (str) a timestamp at which to stop trading, defaults to forever\n        '
    assert (resolution in RESOLUTIONS)
    assert robinhood.logged_in
    self.rbh = robinhood
    self.resolution = resolution
    self.stop_date = until
    self.setup()
    while True:
        date_start = datetime.now()
        timestamp = date_start.isoformat()
        if (self.stop_date and (timestamp > self.stop_date)):
            break
        self._step(timestamp)
        date_end = (date_start + timedelta(seconds=RESOLUTIONS[self.resolution]))
        wait_time = (date_end - datetime.now()).total_seconds()
        if (wait_time <= 0):
            print("Your algo's loop took longer than a timestep!")
        else:
            time.sleep(wait_time)
    self.clean_up()
