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


def rpn_loss(locs, confs, anchors, sizes, bboxes):
    'Loss function for RPN.\n\n     Args:\n         locs (iterable of arrays): An iterable of arrays whose shape is\n             :math:`(N, K_l, 4)`, where :math:`K_l` is the number of\n             the anchor boxes of the :math:`l`-th level.\n         confs (iterable of arrays): An iterable of arrays whose shape is\n             :math:`(N, K_l)`.\n         anchors (list of arrays): A list of arrays returned by\n             :meth:`anchors`.\n         sizes (list of tuples of two ints): A list of\n             :math:`(H_n, W_n)`, where :math:`H_n` and :math:`W_n`\n             are height and width of the :math:`n`-th image.\n         bboxes (list of arrays): A list of arrays whose shape is\n             :math:`(R_n, 4)`, where :math:`R_n` is the number of\n             ground truth bounding boxes.\n\n     Returns:\n         tuple of two variables:\n         :obj:`loc_loss` and :obj:`conf_loss`.\n    '
    fg_thresh = 0.7
    bg_thresh = 0.3
    batchsize_per_image = 256
    fg_ratio = 0.25
    locs = F.concat(locs)
    confs = F.concat(confs)
    xp = cuda.get_array_module(locs.array, confs.array)
    anchors = xp.vstack(anchors)
    anchors_yx = ((anchors[(:, 2:)] + anchors[(:, :2)]) / 2)
    anchors_hw = (anchors[(:, 2:)] - anchors[(:, :2)])
    loc_loss = 0
    conf_loss = 0
    for i in range(len(sizes)):
        if (len(bboxes[i]) > 0):
            iou = utils.bbox_iou(anchors, bboxes[i])
            gt_loc = bboxes[i][iou.argmax(axis=1)].copy()
            gt_loc[(:, 2:)] -= gt_loc[(:, :2)]
            gt_loc[(:, :2)] += (gt_loc[(:, 2:)] / 2)
            gt_loc[(:, :2)] = ((gt_loc[(:, :2)] - anchors_yx) / anchors_hw)
            gt_loc[(:, 2:)] = xp.log((gt_loc[(:, 2:)] / anchors_hw))
        else:
            gt_loc = xp.empty_like(anchors)
        gt_label = xp.empty(len(anchors), dtype=np.int32)
        gt_label[:] = (- 1)
        mask = xp.logical_and((anchors[(:, :2)] >= 0), (anchors[(:, 2:)] < xp.array(sizes[i]))).all(axis=1)
        if (len(bboxes[i]) > 0):
            gt_label[xp.where(mask)[0][(iou[mask] == iou[mask].max(axis=0)).any(axis=1)]] = 1
            gt_label[xp.logical_and(mask, (iou.max(axis=1) >= fg_thresh))] = 1
        fg_index = xp.where((gt_label == 1))[0]
        n_fg = int((batchsize_per_image * fg_ratio))
        if (len(fg_index) > n_fg):
            gt_label[choice(fg_index, size=(len(fg_index) - n_fg))] = (- 1)
        if (len(bboxes[i]) > 0):
            bg_index = xp.where(xp.logical_and(mask, (iou.max(axis=1) < bg_thresh)))[0]
        else:
            bg_index = xp.where(mask)[0]
        n_bg = (batchsize_per_image - int((gt_label == 1).sum()))
        if (len(bg_index) > n_bg):
            gt_label[bg_index[xp.random.randint(len(bg_index), size=n_bg)]] = 0
        n_sample = (gt_label >= 0).sum()
        loc_loss += (F.sum(smooth_l1(locs[i][(gt_label == 1)], gt_loc[(gt_label == 1)], (1 / 9))) / n_sample)
        conf_loss += (F.sum(F.sigmoid_cross_entropy(confs[i][(gt_label >= 0)], gt_label[(gt_label >= 0)], reduce='no')) / n_sample)
    loc_loss /= len(sizes)
    conf_loss /= len(sizes)
    return (loc_loss, conf_loss)
