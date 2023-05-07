import chainer
import chainerx
import os
import sys
import tempfile
from chainer_compiler import _chainer_compiler_core
import cupy
from chainer_compiler import ch2o
import _chainer_compiler_core
import onnx_chainer


def forward(self, *args):
    inputs = list(args)
    flat_inputs = _flatten(inputs)
    runtime_kwargs = {}
    if ((self.runtime_kwargs is not None) and ((self.num_iterations % (self.quiet_period + 1)) == 0)):
        runtime_kwargs.update(self.runtime_kwargs)
    self.num_iterations += 1
    runner = RunCompiledModel(self, inputs, runtime_kwargs)
    outputs = runner.apply((flat_inputs + self.param_values))
    outputs = runner.unflatten_outputs(outputs)
    outputs = outputs[:len(self.orig_output_names)]
    if (len(outputs) == 1):
        outputs = outputs[0]
    return outputs
