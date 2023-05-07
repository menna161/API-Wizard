import argparse
import copy
from datetime import datetime
from enum import Enum
import glob
import importlib
import json
import logging
import math
import numpy as np
import os
import pickle
from pointset import PointSet
import pprint
from queue import Queue
import subprocess
import sys
import tempfile
import tensorflow as tf
import threading
import provider
import tf_util
import pc_util


def prep_pset(pset):
    data64 = np.stack([pset.x, pset.y, pset.z, pset.i, pset.r], axis=1)
    offsets = np.mean(data64[(:, COLUMNS)], axis=0)
    data = (data64[(:, COLUMNS)] - offsets).astype('float32')
    n = len(pset.x)
    if (NUM_POINT < n):
        ixs = np.random.choice(n, NUM_POINT, replace=False)
    elif (NUM_POINT == n):
        ixs = np.arange(NUM_POINT)
    else:
        ixs = np.random.choice(n, NUM_POINT, replace=True)
    return (data64[(ixs, :)], (data[(ixs, :)] / SCALE[COLUMNS]))
