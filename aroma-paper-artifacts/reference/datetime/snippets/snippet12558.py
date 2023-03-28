import inspect
import numpy as np
import re
import os
import sys
from contextlib import contextmanager
from datetime import datetime, timedelta
from tqdm import tqdm
from . import logger
from .concurrency import subproc_call
from ctypes.util import find_library
from ipykernel import iostream


def get_rng(obj=None):
    '\n    Get a good RNG seeded with time, pid and the object.\n\n    Args:\n        obj: some object to use to generate random seed.\n    Returns:\n        np.random.RandomState: the RNG.\n    '
    seed = (((id(obj) + os.getpid()) + int(datetime.now().strftime('%Y%m%d%H%M%S%f'))) % 4294967295)
    if (_RNG_SEED is not None):
        seed = _RNG_SEED
    return np.random.RandomState(seed)
