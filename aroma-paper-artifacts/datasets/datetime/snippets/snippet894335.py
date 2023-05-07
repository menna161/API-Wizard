import re, json, sys, os
import tensorflow as tf
from tqdm import tqdm
from contextlib import closing
from multiprocessing import Pool
from collections import namedtuple
from datetime import datetime, timedelta
from shutil import copyfile as copy_file


def get_time():
    return datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
