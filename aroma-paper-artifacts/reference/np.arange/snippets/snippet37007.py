from __future__ import division
import numpy as np
import chainer
from chainer.backends import cuda
import chainer.functions as F
from chainer import initializers
import chainer.links as L
from chainercv.links.model.fpn.misc import argsort
from chainercv.links.model.fpn.misc import choice
from chainercv.links.model.fpn.misc import exp_clip
from chainercv.links.model.fpn.misc import smooth_l1
from chainercv import utils


def anchors(self, sizes):
    'Calculates anchor boxes.\n\n        Args:\n            sizes (iterable of tuples of two ints): An iterable of\n                :math:`(H_l, W_l)`, where :math:`H_l` and :math:`W_l`\n                are height and width of the :math:`l`-th feature map.\n\n        Returns:\n            list of arrays:\n            The shape of the :math:`l`-th array is :math:`(H_l * W_l * A, 4)`,\n            where :math:`A` is the number of anchor ratios.\n\n        '
    anchors = []
    for (l, (H, W)) in enumerate(sizes):
        (v, u, ar) = np.meshgrid(np.arange(W), np.arange(H), self._anchor_ratios)
        w = np.round(((1 / np.sqrt(ar)) / self._scales[l]))
        h = np.round((w * ar))
        anchor = np.stack((u, v, h, w)).reshape((4, (- 1))).transpose()
        anchor[(:, :2)] = ((anchor[(:, :2)] + 0.5) / self._scales[l])
        anchor[(:, 2:)] *= ((self._anchor_size << l) * self._scales[l])
        anchor[(:, :2)] -= (anchor[(:, 2:)] / 2)
        anchor[(:, 2:)] += anchor[(:, :2)]
        anchors.append(self.xp.array(anchor, dtype=np.float32))
    return anchors
