from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import copy
from six.moves import cPickle as pickle
import logging
import numpy as np
import os
import scipy.sparse
import json
import utils.env as envu
from pycocotools import mask as COCOmask
from pycocotools.coco import COCO
import utils.boxes as box_utils
import utils_rel.boxes_rel as box_utils_rel
from core.config import cfg
from utils.timer import Timer
from .dataset_catalog_rel import ANN_FN
from .dataset_catalog_rel import ANN_FN2
from .dataset_catalog_rel import ANN_FN3
from .dataset_catalog_rel import DATASETS
from .dataset_catalog_rel import IM_DIR
from .dataset_catalog_rel import IM_PREFIX


def _merge_paired_boxes_into_roidb(roidb, sbj_box_list, obj_box_list):
    assert (len(sbj_box_list) == len(obj_box_list) == len(roidb))
    for (i, entry) in enumerate(roidb):
        sbj_boxes = sbj_box_list[i]
        obj_boxes = obj_box_list[i]
        assert (sbj_boxes.shape[0] == obj_boxes.shape[0])
        num_pairs = sbj_boxes.shape[0]
        sbj_gt_overlaps = np.zeros((num_pairs, entry['sbj_gt_overlaps'].shape[1]), dtype=entry['sbj_gt_overlaps'].dtype)
        obj_gt_overlaps = np.zeros((num_pairs, entry['obj_gt_overlaps'].shape[1]), dtype=entry['obj_gt_overlaps'].dtype)
        prd_gt_overlaps = np.zeros((num_pairs, entry['prd_gt_overlaps'].shape[1]), dtype=entry['prd_gt_overlaps'].dtype)
        pair_to_gt_ind_map = (- np.ones(num_pairs, dtype=entry['pair_to_gt_ind_map'].dtype))
        pair_gt_inds = np.arange(entry['prd_gt_classes'].shape[0])
        if (len(pair_gt_inds) > 0):
            sbj_gt_boxes = entry['sbj_gt_boxes'][(pair_gt_inds, :)]
            sbj_gt_classes = entry['sbj_gt_classes'][pair_gt_inds]
            obj_gt_boxes = entry['obj_gt_boxes'][(pair_gt_inds, :)]
            obj_gt_classes = entry['obj_gt_classes'][pair_gt_inds]
            prd_gt_classes = entry['prd_gt_classes'][pair_gt_inds]
            sbj_to_gt_overlaps = box_utils.bbox_overlaps(sbj_boxes.astype(dtype=np.float32, copy=False), sbj_gt_boxes.astype(dtype=np.float32, copy=False))
            obj_to_gt_overlaps = box_utils.bbox_overlaps(obj_boxes.astype(dtype=np.float32, copy=False), obj_gt_boxes.astype(dtype=np.float32, copy=False))
            pair_to_gt_overlaps = np.minimum(sbj_to_gt_overlaps, obj_to_gt_overlaps)
            sbj_argmaxes = sbj_to_gt_overlaps.argmax(axis=1)
            sbj_maxes = sbj_to_gt_overlaps.max(axis=1)
            sbj_I = np.where((sbj_maxes >= 0))[0]
            obj_argmaxes = obj_to_gt_overlaps.argmax(axis=1)
            obj_maxes = obj_to_gt_overlaps.max(axis=1)
            obj_I = np.where((obj_maxes >= 0))[0]
            pair_argmaxes = pair_to_gt_overlaps.argmax(axis=1)
            pair_maxes = pair_to_gt_overlaps.max(axis=1)
            pair_I = np.where((pair_maxes >= 0))[0]
            sbj_gt_overlaps[(sbj_I, sbj_gt_classes[sbj_argmaxes[sbj_I]])] = sbj_maxes[sbj_I]
            obj_gt_overlaps[(obj_I, obj_gt_classes[obj_argmaxes[obj_I]])] = obj_maxes[obj_I]
            prd_gt_overlaps[(pair_I, prd_gt_classes[pair_argmaxes[pair_I]])] = pair_maxes[pair_I]
            pair_to_gt_ind_map[pair_I] = pair_gt_inds[pair_argmaxes[pair_I]]
        entry['sbj_boxes'] = sbj_boxes.astype(entry['sbj_gt_boxes'].dtype, copy=False)
        entry['sbj_gt_overlaps'] = sbj_gt_overlaps
        entry['sbj_gt_overlaps'] = scipy.sparse.csr_matrix(entry['sbj_gt_overlaps'])
        entry['obj_boxes'] = obj_boxes.astype(entry['obj_gt_boxes'].dtype, copy=False)
        entry['obj_gt_overlaps'] = obj_gt_overlaps
        entry['obj_gt_overlaps'] = scipy.sparse.csr_matrix(entry['obj_gt_overlaps'])
        entry['prd_gt_classes'] = (- np.ones(num_pairs, dtype=entry['prd_gt_classes'].dtype))
        entry['prd_gt_overlaps'] = prd_gt_overlaps
        entry['prd_gt_overlaps'] = scipy.sparse.csr_matrix(entry['prd_gt_overlaps'])
        entry['pair_to_gt_ind_map'] = pair_to_gt_ind_map.astype(entry['pair_to_gt_ind_map'].dtype, copy=False)
