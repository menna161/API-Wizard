import os
import pytest
import sys
import chainer
from chainer.backend import CpuDevice
import chainer.functions as F
import chainer.links as L
import chainerx.testing
import numpy as np
from chainer_compiler import chainer_compiler
import cupy
import onnx_chainer


def aranges(xp, *shape):
    r = np.prod(shape)
    return np.arange(r).reshape(shape).astype(np.float32)
