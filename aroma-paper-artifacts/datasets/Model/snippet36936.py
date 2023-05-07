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


def compile_onnx(model, onnx_file, used_translator, **kwargs):
    return CompiledModel(model, onnx_file, used_translator, **kwargs)
