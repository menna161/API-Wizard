import chainer
import chainer.functions as F
import chainer.links as L
import numpy as np
import onnx
import onnx_script
import test_case
import gen_chainercv_op_tests
import sentiment


def aranges(*shape):
    r = np.prod(shape)
    return np.arange(r).reshape(shape).astype(np.float32)
