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


def compile(model, inputs, translator='ch2o', **kwargs):
    onnx_file = export(model, inputs, filename=None, translator=translator)
    compiled_model = CompiledModel(model, onnx_file, translator, **kwargs)
    return compiled_model
