import os
import numpy as np
import datetime
from data.AgricultureVision.loader import *


def write2txt(self):
    file = open(os.path.join(self.save_path, (str(datetime.datetime.now()) + '.txt')), 'w')
    for a in dir(self):
        if ((not a.startswith('__')) and (not callable(getattr(self, a)))):
            line = '{:30} {}'.format(a, getattr(self, a))
            file.write((line + '\n'))
