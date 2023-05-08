from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from collections import defaultdict
import cv2
import datetime
import logging
import numpy as np
from numpy import linalg as la
import os
import yaml
import json
from six.moves import cPickle as pickle
import torch
import nn as mynn
from torch.autograd import Variable
import importlib
from core.config import cfg
from core.test_rel import im_detect_rels
from datasets_rel import task_evaluation_sg as task_evaluation_sg
from datasets_rel import task_evaluation_vg_and_vrd as task_evaluation_vg_and_vrd
from datasets_rel.json_dataset_rel import JsonDatasetRel
from modeling_rel import fusion_256pairs as model_builder_rel
from utils.detectron_weight_helper import load_detectron_weight
import utils.env as envu
import utils_rel.net_rel as net_utils_rel
import utils_rel.subprocess_rel as subprocess_utils
import utils.vis as vis_utils
from utils.io import save_object
from utils.timer import Timer


def get_metrics_det_boxes(model, timers, dataset_name):
    model.eval()
    (roidb, dataset, start_ind, end_ind, total_num_images) = get_roidb_and_dataset(dataset_name, None, None, True)
    num_images = len(roidb)
    all_results = [None for _ in range(num_images)]
    for (i, entry) in enumerate(roidb):
        box_proposals = None
        im = cv2.imread(entry['image'])
        im_results = im_detect_rels(model, im, dataset_name, box_proposals, False, timers)
        im_results.update(dict(image=entry['image']))
        im_results.update(dict(gt_sbj_boxes=entry['sbj_gt_boxes'], gt_sbj_labels=entry['sbj_gt_classes'], gt_obj_boxes=entry['obj_gt_boxes'], gt_obj_labels=entry['obj_gt_classes'], gt_prd_labels=entry['prd_gt_classes']))
        all_results[i] = im_results
    if ((dataset_name.find('vg') >= 0) or (dataset_name.find('vrd') >= 0)):
        metrics = task_evaluation_vg_and_vrd.eval_rel_results(all_results, None, True)
    else:
        metrics = task_evaluation_sg.eval_rel_results(all_results, None, True)
    return metrics
