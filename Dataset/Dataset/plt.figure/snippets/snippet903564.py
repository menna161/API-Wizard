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


def plot_memory_usage(self, plot_file):
    '\n        Plots memory usage for each operator in the schedule as a stacked bar chart.\n        :param plot_file: Output file\n        '
    import matplotlib.pyplot as plt
    labels = []
    input_sizes = []
    output_sizes = []
    other_sizes = []
    schedule = self._execution_schedule_info()
    peak_mem_use = 0
    for (op, working_set, mem_use, _, _) in schedule:
        input_size = TFLiteModel._cum_tensor_sizes(op.non_empty_inputs)
        output_size = op.output.size
        other_size = TFLiteModel._cum_tensor_sizes((t for t in working_set if ((t not in op.non_empty_inputs) and (t != op.output))))
        assert (((input_size + output_size) + other_size) == mem_use)
        peak_mem_use = max(peak_mem_use, mem_use)
        labels.append(op.output.name)
        input_sizes.append(input_size)
        output_sizes.append(output_size)
        other_sizes.append(other_size)
    input_sizes = (np.array(input_sizes) / 1024)
    output_sizes = (np.array(output_sizes) / 1024)
    other_sizes = (np.array(other_sizes) / 1024)
    peak_mem_use /= 1024
    fig = plt.figure(figsize=(max((len(labels) / 3.5), 6), 8))
    fig.tight_layout()
    ax = fig.gca()
    x = np.arange(0, len(labels))
    ax.bar(x, input_sizes, color='#D95319', label='Operator inputs')
    ax.bar(x, output_sizes, bottom=input_sizes, color='#EDB120', label='Operator outputs')
    ax.bar(x, other_sizes, bottom=(input_sizes + output_sizes), color='#0072BD', label='Other tensors')
    ax.set_xticks(x)
    ax.set_xlabel('Operators')
    ax.set_ylabel('Memory usage (KB)')
    ax.set_ylim([0, (peak_mem_use + 10)])
    ax.set_xticklabels(labels, rotation=90)
    ax.legend()
    plt.savefig(plot_file, bbox_inches='tight', dpi=300)
