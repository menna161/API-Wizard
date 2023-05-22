import os
import sys
import chainerx
import chainerx.testing
import numpy as np
import onnx
import _chainer_compiler_core
import onnx_script


def aranges(*shape):
    r = np.prod(shape)
    return chainerx.array(np.arange(r).reshape(shape).astype(np.float32))
