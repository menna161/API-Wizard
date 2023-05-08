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


def test_net(args, dataset_name, proposal_file, output_dir, ind_range=None, gpu_id=0):
    'Run inference on all images in a dataset or over an index range of images\n    in a dataset using a single GPU.\n    '
    assert (not cfg.MODEL.RPN_ONLY), 'Use rpn_generate to generate proposals from RPN-only models'
    (roidb, dataset, start_ind, end_ind, total_num_images) = get_roidb_and_dataset(dataset_name, proposal_file, ind_range, args.do_val)
    model = initialize_model_from_cfg(args, gpu_id=gpu_id)
    num_images = len(roidb)
    all_results = [None for _ in range(num_images)]
    timers = defaultdict(Timer)
    for (i, entry) in enumerate(roidb):
        box_proposals = None
        im = cv2.imread(entry['image'])
        if args.use_gt_boxes:
            im_results = im_detect_rels(model, im, dataset_name, box_proposals, args.do_vis, timers, entry, args.use_gt_labels)
        else:
            im_results = im_detect_rels(model, im, dataset_name, box_proposals, args.do_vis, timers)
        im_results.update(dict(image=entry['image']))
        if args.do_val:
            im_results.update(dict(gt_sbj_boxes=entry['sbj_gt_boxes'], gt_sbj_labels=entry['sbj_gt_classes'], gt_obj_boxes=entry['obj_gt_boxes'], gt_obj_labels=entry['obj_gt_classes'], gt_prd_labels=entry['prd_gt_classes']))
        all_results[i] = im_results
        if ((i % 10) == 0):
            ave_total_time = np.sum([t.average_time for t in timers.values()])
            eta_seconds = (ave_total_time * ((num_images - i) - 1))
            eta = str(datetime.timedelta(seconds=int(eta_seconds)))
            det_time = timers['im_detect_rels'].average_time
            logger.info('im_detect: range [{:d}, {:d}] of {:d}: {:d}/{:d} {:.3f}s (eta: {})'.format((start_ind + 1), end_ind, total_num_images, ((start_ind + i) + 1), (start_ind + num_images), det_time, eta))
    cfg_yaml = yaml.dump(cfg)
    if (ind_range is not None):
        det_name = ('rel_detection_range_%s_%s.pkl' % tuple(ind_range))
    elif args.use_gt_boxes:
        if args.use_gt_labels:
            det_name = (('rel_detections_gt_boxes_prdcls_' + args.load_ckpt.split('_')[(- 1)].split('.')[(- 2)]) + '.pkl')
        else:
            det_name = (('rel_detections_gt_boxes_sgcls_' + args.load_ckpt.split('_')[(- 1)].split('.')[(- 2)]) + '.pkl')
    else:
        det_name = (('rel_detections_' + args.load_ckpt.split('_')[(- 1)].split('.')[(- 2)]) + '.pkl')
    det_file = os.path.join(output_dir, det_name)
    save_object(all_results, det_file)
    logger.info('Wrote rel_detections to: {}'.format(os.path.abspath(det_file)))
    return all_results
