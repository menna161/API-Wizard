from __future__ import division
import numpy as np
import chainer
from chainer.backends import cuda
import chainer.functions as F
from chainer.initializers import HeNormal
import chainer.links as L
from testcases.elichika_tests.chainercv_model.utils import Conv2DActiv
from testcases.elichika_tests.chainercv_model.utils.bbox.bbox_iou import bbox_iou
from testcases.elichika_tests.chainercv_model.fpn.mask_utils import mask_to_segm
from testcases.elichika_tests.chainercv_model.fpn.mask_utils import segm_to_mask


def __init__(self, n_class, scales):
    super(MaskHead, self).__init__()
    initialW = HeNormal(1, fan_option='fan_out')
    with self.init_scope():
        self.conv1 = Conv2DActiv(256, 3, pad=1, initialW=initialW)
        self.conv2 = Conv2DActiv(256, 3, pad=1, initialW=initialW)
        self.conv3 = Conv2DActiv(256, 3, pad=1, initialW=initialW)
        self.conv4 = Conv2DActiv(256, 3, pad=1, initialW=initialW)
        self.conv5 = L.Deconvolution2D(256, 2, pad=0, stride=2, initialW=initialW)
        self.seg = L.Convolution2D(n_class, 1, pad=0, initialW=initialW)
    self._n_class = n_class
    self._scales = scales
