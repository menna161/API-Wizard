import tensorflow as tf
from contextlib import contextmanager
from tensorpack.tfutils.argscope import argscope
from tensorpack.tfutils.varreplace import remap_variables
from tensorpack.models import Conv2D, MaxPooling, GlobalAvgPooling, BatchNorm, FullyConnected, BNReLU, layer_register


@contextmanager
def weight_standardization_context(enable=True):
    "\n    Implement Centered Weight Normalization\n    (http://openaccess.thecvf.com/content_ICCV_2017/papers/Huang_Centered_Weight_Normalization_ICCV_2017_paper.pdf)\n    or Weight Standardization (https://arxiv.org/abs/1903.10520)\n\n    Usage:\n\n    with weight_standardization_context():\n        l = Conv2D('conv', l)\n        ...\n    "
    if enable:

        def weight_standardization(v):
            if ((not v.name.endswith('/W:0')) or (v.shape.ndims != 4)):
                return v
            (mean, var) = tf.nn.moments(v, [0, 1, 2], keep_dims=True)
            v = ((v - mean) / (tf.sqrt(var) + 1e-05))
            return v
        with remap_variables(weight_standardization):
            (yield)
    else:
        (yield)
