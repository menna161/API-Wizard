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


def optimize_memory(self):
    (_, op_order) = self.compute_best_peak_memory_usage()
    num_operators = len(self.model_graph.operators)
    correctly_ordered = all(((i == op_order[i].id) for i in range(num_operators)))
    if correctly_ordered:
        print('The model already has optimal operator order.')
        return
    model = Model.Model.GetRootAsModel(self.model_bytes, 0)
    subgraph = model.Subgraphs(0)
    indirection_table_offset = UOffsetTFlags.py_type(subgraph._tab.Offset(10))
    indirection_table = subgraph._tab.GetVectorAsNumpy(UOffsetTFlags, indirection_table_offset)
    old_indirection_table = indirection_table.copy()
    for i in range(num_operators):
        op_id = op_order[i].id
        indirection_table[i] = (old_indirection_table[op_id] + (4 * (op_id - i)))
        op_order[i].id = i
    self.model_graph.operators.sort(key=(lambda op: op.id))
