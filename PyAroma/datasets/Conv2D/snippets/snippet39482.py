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


def distribute(self, rois, roi_indices):
    'Assigns feature levels to Rois based on their size.\n\n        Args:\n            rois (array): An array of shape :math:`(R, 4)`,                 where :math:`R` is the total number of RoIs in the given batch.\n            roi_indices (array): An array of shape :math:`(R,)`.\n\n        Returns:\n            two lists and one array:\n            :obj:`out_rois`, :obj:`out_roi_indices` and :obj:`order`.\n\n            * **out_rois**: A list of arrays of shape :math:`(R_l, 4)`,                 where :math:`R_l` is the number of RoIs in the :math:`l`-th                 feature map.\n            * **out_roi_indices** : A list of arrays of shape :math:`(R_l,)`.\n            * **order**: A correspondence between the output and the input.                 The relationship below is satisfied.\n\n            .. code:: python\n\n                xp.concatenate(out_rois, axis=0)[order[i]] == rois[i]\n\n        '
    size = self.xp.sqrt(self.xp.prod((rois[(:, 2:)] - rois[(:, :2)]), axis=1))
    level = self.xp.floor(self.xp.log2(((size / self._canonical_scale) + 1e-06))).astype(np.int32)
    level = self.xp.clip((level + self._canonical_level), 0, (len(self._scales) - 2))
    masks = [(level == l) for l in range(len(self._scales))]
    out_rois = [rois[mask] for mask in masks]
    out_roi_indices = [roi_indices[mask] for mask in masks]
    order = self.xp.argsort(self.xp.concatenate([self.xp.where(mask)[0] for mask in masks]))
    return (out_rois, out_roi_indices, order)
