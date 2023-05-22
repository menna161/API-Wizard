import chainer
import chainer.functions as F
import chainer.links as L
import numpy as np
import onnx
import onnx_script
import test_case
import chainercv_rpn


def aranges(*shape):
    r = np.prod(shape)
    v = np.arange(r).reshape(shape).astype(np.float32)
    v -= ((r / 2) + 0.1)
    return v
