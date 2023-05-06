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


def mask_head_loss_post(segms, mask_roi_indices, gt_segms, gt_mask_labels, batchsize):
    'Loss function for Mask Head (post).\n\n     Args:\n         segms (array): An array whose shape is :math:`(R, n\\_class, M, M)`,\n             where :math:`R` is the total number of RoIs in the given batch.\n         mask_roi_indices (array): A list of arrays returned by\n             :func:`mask_head_loss_pre`.\n         gt_segms (list of arrays): A list of arrays returned by\n             :func:`mask_head_loss_pre`.\n         gt_mask_labels (list of arrays): A list of arrays returned by\n             :func:`mask_head_loss_pre`.\n         batchsize (int): The size of batch.\n\n     Returns:\n        chainer.Variable:\n        Mask loss.\n    '
    xp = cuda.get_array_module(segms.array)
    mask_roi_indices = xp.hstack(mask_roi_indices).astype(np.int32)
    gt_segms = xp.vstack(gt_segms)
    gt_mask_labels = xp.hstack(gt_mask_labels).astype(np.int32)
    mask_loss = F.sigmoid_cross_entropy(segms[(np.arange(len(gt_mask_labels)), gt_mask_labels)], gt_segms.astype(np.int32))
    return mask_loss
