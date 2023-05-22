import numpy as np
import os
from glob import glob
import shutil
from datetime import datetime
from scipy.ndimage import imread


def get_date_str():
    '\n    @return: A string representing the current date/time that can be used as a directory name.\n    '
    return str(datetime.now()).replace(' ', '_').replace(':', '.')[:(- 10)]
