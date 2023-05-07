import sys
import csv
from collections import namedtuple
import functools
from pathlib import Path
from .tflite import Model
from .tflite.BuiltinOperator import BuiltinOperator
from .tflite.TensorType import TensorType
from flatbuffers.number_types import UOffsetTFlags
import numpy as np
from prettytable import PrettyTable
from . import tflite
from sklearn import cluster
import matplotlib.pyplot as plt
from tflite.Pool2DOptions import Pool2DOptions


def _overwrite_flatbuffers_buffer(self, buffer_idx, new_contents):
    model = Model.Model.GetRootAsModel(self.model_bytes, 0)
    orig_buffer = model.Buffers(buffer_idx)
    orig_buffer.DataAsNumpy()[:] = new_contents.astype(np.uint8).flatten()
