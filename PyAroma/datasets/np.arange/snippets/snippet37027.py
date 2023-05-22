import shutil
import chainer
import numpy as np
import onnx_chainer
from test_case import TestCase


def aranges(*shape):
    r = np.prod(shape)
    return np.arange(r).reshape(shape).astype(np.float32)
