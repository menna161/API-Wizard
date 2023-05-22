import copy
from os.path import join
from datetime import datetime
import numpy as np
import pandas as pd
import yaml
from common import get_logger


def _date_parser(millisecs):
    if np.isnan(float(millisecs)):
        return millisecs
    return datetime.fromtimestamp(float(millisecs))
