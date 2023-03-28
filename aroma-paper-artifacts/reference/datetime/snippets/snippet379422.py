import argparse
import datetime
import glob
import math
import os
from os.path import join, isfile
import logging
import sys
import time
import yaml
from filelock import FileLock
import psutil
import pandas as pd
from sklearn.metrics import mean_squared_error


def _detect_ingestion_alive(args):
    start_filepath = join(args.prediction_dir, 'start.txt')
    lockfile = join(args.prediction_dir, 'start.txt.lock')
    if (not os.path.exists(start_filepath)):
        return False
    with FileLock(lockfile):
        with open(start_filepath, 'r') as ftmp:
            try:
                last_time = datetime.datetime.fromtimestamp(yaml.safe_load(ftmp))
            except Exception:
                LOGGER.info(f'the content of start.txt is: {ftmp.read()}')
                raise
    current_time = datetime.datetime.now()
    timediff = (current_time - last_time)
    if (timediff > MAX_TIME_DIFF):
        return False
    return True
