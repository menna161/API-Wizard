import os
import sys
import chainer
import numpy as np
import onnx
from test_case import TestCase
from chainer_compiler import ch2o


def aranges(*shape):
    r = np.prod(shape)
    return np.arange(r).reshape(shape).astype(np.float32)
