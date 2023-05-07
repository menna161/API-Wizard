import mxnet as mx
import numpy as np
import time
import os
import logging
from datetime import datetime
from subprocess import call
from types import ModuleType


def getTime():
    return datetime.now().strftime('%m-%d %H:%M:%S')
