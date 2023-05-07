import os
import os.path as osp
import mmcv
import numpy as np
import torch
import torch.distributed as dist
from mmcv.runner import Hook, obj_from_dict
from mmcv.parallel import scatter, collate
from pycocotools.cocoeval import COCOeval
from torch.utils.data import Dataset
from .coco_utils import results2json, fast_eval_recall
from .mean_ap import eval_map
from mmdet import datasets


def __init__(self, dataset, interval=1, proposal_nums=(100, 300, 1000), iou_thrs=np.arange(0.5, 0.96, 0.05)):
    super(CocoDistEvalRecallHook, self).__init__(dataset, interval=interval)
    self.proposal_nums = np.array(proposal_nums, dtype=np.int32)
    self.iou_thrs = np.array(iou_thrs, dtype=np.float32)
