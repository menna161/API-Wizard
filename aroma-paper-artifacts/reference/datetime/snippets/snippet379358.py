import os
from os.path import join
import sys
from sys import path
import argparse
import datetime
import subprocess
import threading
import time
import numpy as np
import yaml
from filelock import FileLock
from common import get_logger, init_usermodel
import timing
from timing import Timer
from dataset import Dataset


def write_start_file(output_dir):
    "Create start file 'start.txt' in `output_dir` with updated timestamp\n    start time.\n\n    "
    LOGGER.info('===== alive_thd started')
    start_filepath = os.path.join(output_dir, 'start.txt')
    lockfile = os.path.join(output_dir, 'start.txt.lock')
    while True:
        current_time = datetime.datetime.now().timestamp()
        with FileLock(lockfile):
            with open(start_filepath, 'w') as ftmp:
                yaml.dump(current_time, ftmp)
        time.sleep(10)
