import chainer
import chainer.functions as F
from testcases.elichika_tests.chainercv_model.utils import Conv2DBNActiv
from testcases.elichika_tests.chainercv_model.utils import PickableSequentialChain
from testcases.elichika_tests.chainercv_model.utils import SEBlock
from chainer_compiler.elichika.parser import flags
from chainer_compiler.elichika import testtools
from chainer import initializers
import numpy as np


def __init__(self, in_channels, mid_channels, out_channels, stride=1, dilate=1, groups=1, initialW=None, bn_kwargs={}, residual_conv=False, stride_first=False, add_seblock=False):
    if stride_first:
        first_stride = stride
        second_stride = 1
    else:
        first_stride = 1
        second_stride = stride
    super(Bottleneck, self).__init__()
    with self.init_scope():
        self.conv1 = Conv2DBNActiv(in_channels, mid_channels, 1, first_stride, 0, nobias=True, initialW=initialW, bn_kwargs=bn_kwargs)
        self.conv2 = Conv2DBNActiv(mid_channels, mid_channels, 3, second_stride, dilate, dilate, groups, nobias=True, initialW=initialW, bn_kwargs=bn_kwargs)
        self.conv3 = Conv2DBNActiv(mid_channels, out_channels, 1, 1, 0, nobias=True, initialW=initialW, activ=None, bn_kwargs=bn_kwargs)
        self._pick = ('conv3',)
        if add_seblock:
            self.se = SEBlock(out_channels)
            self._pick = ('se',)
        if residual_conv:
            self.residual_conv = Conv2DBNActiv(in_channels, out_channels, 1, stride, 0, nobias=True, initialW=initialW, activ=None, bn_kwargs=bn_kwargs)
            self._pick = ('residual_conf',)
        self._return_tuple = False
