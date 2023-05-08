import os
import pika
from multiprocessing.pool import ThreadPool
import threading
import pickle
from functools import partial
from typing import Tuple
from queue import Queue
import time
from abc import ABCMeta, abstractmethod
import sys
import functools
import termcolor
import datetime
import traceback
import traceback
import traceback


def info_prefix():
    return '[{} info]'.format(datetime.datetime(1, 1, 1).now())
