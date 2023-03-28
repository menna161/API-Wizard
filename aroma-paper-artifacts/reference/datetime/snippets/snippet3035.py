import os
import os.path as osp
import sys
import numpy as np
from datetime import datetime
from glob import glob
from itertools import chain
import gc
from .logger import red, green, yellow
import cv2
from contextlib import contextmanager
import subprocess
import subprocess
from IPython import embed


def random_int(obj=None):
    return (((id(obj) + os.getpid()) + int(datetime.now().strftime('%Y%m%d%H%M%S%f'))) % 4294967295)
