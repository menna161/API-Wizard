import sys
import os
import gzip
import numpy as np
import pickle
import scipy.io as sio
import h5py
import urllib.request as request
from urllib2 import Request as request


def to_one_hot(x, depth):
    ret = np.zeros((x.shape[0], depth), dtype=np.int32)
    ret[(np.arange(x.shape[0]), x)] = 1
    return ret
