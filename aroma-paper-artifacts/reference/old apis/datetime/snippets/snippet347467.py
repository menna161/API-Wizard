import datetime as dt
import glob
import os
from collections import namedtuple
import numpy as np
import pykitti.utils as utils


def _load_timestamps(self):
    'Load timestamps from file.'
    timestamp_file = os.path.join(self.data_path, 'oxts', 'timestamps.txt')
    self.timestamps = []
    with open(timestamp_file, 'r') as f:
        for line in f.readlines():
            t = dt.datetime.strptime(line[:(- 4)], '%Y-%m-%d %H:%M:%S.%f')
            self.timestamps.append(t)
    if (self.frames is not None):
        self.timestamps = [self.timestamps[i] for i in self.frames]
