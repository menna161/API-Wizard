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


def decode(self, segms, bboxes, labels, sizes):
    "Decodes back to masks.\n\n        Args:\n            segms (iterable of arrays): An iterable of arrays of\n                shape :math:`(R_n, n\\_class, M, M)`.\n            bboxes (iterable of arrays): An iterable of arrays of\n                shape :math:`(R_n, 4)`.\n            labels (iterable of arrays): An iterable of arrays of\n                shape :math:`(R_n,)`.\n            sizes (list of tuples of two ints): A list of\n                :math:`(H_n, W_n)`, where :math:`H_n` and :math:`W_n`\n                are height and width of the :math:`n`-th image.\n\n        Returns:\n            list of arrays:\n            This list contains instance segmentation for each image\n            in the batch.\n            More precisely, this is a list of boolean arrays of shape\n            :math:`(R'_n, H_n, W_n)`, where :math:`R'_n` is the number of\n            bounding boxes in the :math:`n`-th image.\n        "
    xp = chainer.backends.cuda.get_array_module(*segms)
    if (xp != np):
        raise ValueError('MaskHead.decode only supports numpy inputs for now.')
    masks = []
    for (bbox, segm, label, size) in zip(bboxes, segms, labels, sizes):
        if (len(segm) > 0):
            masks.append(segm_to_mask(segm[(np.arange(len(label)), (label + 1))], bbox, size))
        else:
            masks.append(np.zeros(((0,) + size), dtype=np.bool))
    return masks
