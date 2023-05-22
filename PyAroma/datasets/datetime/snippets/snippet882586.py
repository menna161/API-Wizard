import torch
from torch import Tensor
from torch.utils import data
import pandas as pd
import numpy as np
import datetime as dt
import os
import json


def interval_days(date1, date2):
    return abs((dt.datetime(*parse(date1)) - dt.datetime(*parse(date2))).days)
