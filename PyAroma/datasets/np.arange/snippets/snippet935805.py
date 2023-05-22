import numpy as np
from terminaltables import AsciiTable
from .bbox_overlaps import bbox_overlaps
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt


def _recalls(all_ious, proposal_nums, thrs):
    img_num = all_ious.shape[0]
    total_gt_num = sum([ious.shape[0] for ious in all_ious])
    _ious = np.zeros((proposal_nums.size, total_gt_num), dtype=np.float32)
    for (k, proposal_num) in enumerate(proposal_nums):
        tmp_ious = np.zeros(0)
        for i in range(img_num):
            ious = all_ious[i][(:, :proposal_num)].copy()
            gt_ious = np.zeros(ious.shape[0])
            if (ious.size == 0):
                tmp_ious = np.hstack((tmp_ious, gt_ious))
                continue
            for j in range(ious.shape[0]):
                gt_max_overlaps = ious.argmax(axis=1)
                max_ious = ious[(np.arange(0, ious.shape[0]), gt_max_overlaps)]
                gt_idx = max_ious.argmax()
                gt_ious[j] = max_ious[gt_idx]
                box_idx = gt_max_overlaps[gt_idx]
                ious[(gt_idx, :)] = (- 1)
                ious[(:, box_idx)] = (- 1)
            tmp_ious = np.hstack((tmp_ious, gt_ious))
        _ious[(k, :)] = tmp_ious
    _ious = np.fliplr(np.sort(_ious, axis=1))
    recalls = np.zeros((proposal_nums.size, thrs.size))
    for (i, thr) in enumerate(thrs):
        recalls[(:, i)] = ((_ious >= thr).sum(axis=1) / float(total_gt_num))
    return recalls
