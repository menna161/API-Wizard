import torch
from mmdet.utils import util_mixins
from mmdet.core.bbox import demodata
import numpy as np


@classmethod
def random(cls, **kwargs):
    '\n        Create random AssignResult for tests or debugging.\n\n        Kwargs:\n            num_preds: number of predicted boxes\n            num_gts: number of true boxes\n            p_ignore (float): probability of a predicted box assinged to an\n                ignored truth\n            p_assigned (float): probability of a predicted box not being\n                assigned\n            p_use_label (float | bool): with labels or not\n            rng (None | int | numpy.random.RandomState): seed or state\n\n        Returns:\n            AssignResult :\n\n        Example:\n            >>> from mmdet.core.bbox.assigners.assign_result import *  # NOQA\n            >>> self = AssignResult.random()\n            >>> print(self.info)\n        '
    from mmdet.core.bbox import demodata
    rng = demodata.ensure_rng(kwargs.get('rng', None))
    num_gts = kwargs.get('num_gts', None)
    num_preds = kwargs.get('num_preds', None)
    p_ignore = kwargs.get('p_ignore', 0.3)
    p_assigned = kwargs.get('p_assigned', 0.7)
    p_use_label = kwargs.get('p_use_label', 0.5)
    num_classes = kwargs.get('p_use_label', 3)
    if (num_gts is None):
        num_gts = rng.randint(0, 8)
    if (num_preds is None):
        num_preds = rng.randint(0, 16)
    if (num_gts == 0):
        max_overlaps = torch.zeros(num_preds, dtype=torch.float32)
        gt_inds = torch.zeros(num_preds, dtype=torch.int64)
        if ((p_use_label is True) or (p_use_label < rng.rand())):
            labels = torch.zeros(num_preds, dtype=torch.int64)
        else:
            labels = None
    else:
        import numpy as np
        max_overlaps = torch.from_numpy(rng.rand(num_preds))
        is_assigned = torch.from_numpy((rng.rand(num_preds) < p_assigned))
        n_assigned = min(num_preds, min(num_gts, is_assigned.sum()))
        assigned_idxs = np.where(is_assigned)[0]
        rng.shuffle(assigned_idxs)
        assigned_idxs = assigned_idxs[0:n_assigned]
        assigned_idxs.sort()
        is_assigned[:] = 0
        is_assigned[assigned_idxs] = True
        is_ignore = (torch.from_numpy((rng.rand(num_preds) < p_ignore)) & is_assigned)
        gt_inds = torch.zeros(num_preds, dtype=torch.int64)
        true_idxs = np.arange(num_gts)
        rng.shuffle(true_idxs)
        true_idxs = torch.from_numpy(true_idxs)
        gt_inds[is_assigned] = true_idxs[:n_assigned]
        gt_inds = torch.from_numpy(rng.randint(1, (num_gts + 1), size=num_preds))
        gt_inds[is_ignore] = (- 1)
        gt_inds[(~ is_assigned)] = 0
        max_overlaps[(~ is_assigned)] = 0
        if ((p_use_label is True) or (p_use_label < rng.rand())):
            if (num_classes == 0):
                labels = torch.zeros(num_preds, dtype=torch.int64)
            else:
                labels = torch.from_numpy(rng.randint(1, (num_classes + 1), size=num_preds))
                labels[(~ is_assigned)] = 0
        else:
            labels = None
    self = cls(num_gts, gt_inds, max_overlaps, labels)
    return self
