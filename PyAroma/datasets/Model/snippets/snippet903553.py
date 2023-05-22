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


def _build_graph(self):
    model = Model.Model.GetRootAsModel(self.model_bytes, 0)
    subgraph = model.Subgraphs(0)
    tensors = []
    operators = []
    for i in range(subgraph.TensorsLength()):
        t = subgraph.Tensors(i)
        tensors.append(TFLiteTensor(id=i, shape=t.ShapeAsNumpy(), name=t.Name().decode('ascii'), producer=None, consumers=[], type=t.Type()))
    for i in range(subgraph.OperatorsLength()):
        op = subgraph.Operators(i)
        assert (op.OutputsLength() <= 1)
        has_output = (op.OutputsLength() == 1)
        inputs = [(tensors[j] if (j != (- 1)) else None) for j in op.InputsAsNumpy()]
        assert (len(inputs) > 0)
        opcode = model.OperatorCodes(op.OpcodeIndex()).BuiltinCode()
        tflite_op = TFLiteOperator(id=i, output=(tensors[op.Outputs(0)] if has_output else None), inputs=inputs, opcode=opcode, options=op.BuiltinOptions())
        tflite_op.output.producer = tflite_op
        for t in tflite_op.non_empty_inputs:
            t.consumers.append(tflite_op)
        operators.append(tflite_op)
    inputs = [tensors[j] for j in subgraph.InputsAsNumpy()]
    outputs = [tensors[j] for j in subgraph.OutputsAsNumpy()]
    for t in tensors:
        t.is_constant = ((t.producer is None) and (t not in inputs))

    def _compute_predecessors(tensor):
        if (tensor.predecessors is not None):
            return tensor.predecessors
        if (tensor.producer is None):
            tensor.predecessors = set()
        else:
            op_inputs = tensor.producer.non_empty_inputs
            tensor.predecessors = set(op_inputs)
            for i in op_inputs:
                tensor.predecessors |= _compute_predecessors(i)
        return tensor.predecessors
    for o in outputs:
        _compute_predecessors(o)
    self.model_graph = TFLiteGraph(tensors, operators, inputs, outputs)
