import json
import torch
import numpy as np
from datetime import datetime
from collections import namedtuple
import tensorflow as tf
import matplotlib.pyplot as plt


def timer(func):

    def wrapper(*args, **kwds):
        start_t = datetime.now()
        rets = func(*args, **kwds)
        end_t = datetime.now()
        if (rets is not None):
            return (*rets, (end_t - start_t))
        else:
            return (end_t - start_t)
    return wrapper
