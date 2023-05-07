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


def _discover_tflite_weights(self):
    model = Model.Model.GetRootAsModel(self.model_bytes, 0)
    subgraph = model.Subgraphs(0)
    weights = []
    for o in range(subgraph.OperatorsLength()):
        op = subgraph.Operators(o)
        opcode = model.OperatorCodes(op.OpcodeIndex()).BuiltinCode()
        inputs = op.InputsAsNumpy()
        parametrised_opcodes = [BuiltinOperator.CONV_2D, BuiltinOperator.FULLY_CONNECTED, BuiltinOperator.DEPTHWISE_CONV_2D]
        if (opcode not in parametrised_opcodes):
            continue
        weight_tensor = subgraph.Tensors(inputs[1])
        buffer_idx = weight_tensor.Buffer()
        buffer = model.Buffers(buffer_idx)
        weights.append((buffer_idx, get_buffer_as_numpy(weight_tensor, buffer)))
    return weights
