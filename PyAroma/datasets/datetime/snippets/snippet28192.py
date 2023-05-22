import re
import numpy as np
import tensorflow as tf
from itertools import takewhile, repeat
from typing import List, Optional, Tuple, Iterable
from datetime import datetime
from collections import OrderedDict


@staticmethod
def now_str():
    return datetime.now().strftime('%Y%m%d-%H%M%S: ')
