from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from collections import defaultdict
import cv2
import datetime
import logging
import numpy as np
import os
import yaml
from caffe2.python import workspace
from detectron.core.config import cfg
from detectron.core.config import get_output_dir
from detectron.core.rpn_generator import generate_rpn_on_dataset
from detectron.core.rpn_generator import generate_rpn_on_range
from detectron.core.test import im_detect_all
from detectron.datasets import task_evaluation
from detectron.datasets.json_dataset import JsonDataset
from detectron.modeling import model_builder
from detectron.utils.io import save_object
from detectron.utils.timer import Timer
import detectron.utils.c2 as c2_utils
import detectron.utils.env as envu
import detectron.utils.net as net_utils
import detectron.utils.subprocess as subprocess_utils
import detectron.utils.vis as vis_utils


def test_net(weights_file, dataset_name, proposal_file, output_dir, ind_range=None, gpu_id=0):
    'Run inference on all images in a dataset or over an index range of images\n    in a dataset using a single GPU.\n    '
    assert (not cfg.MODEL.RPN_ONLY), 'Use rpn_generate to generate proposals from RPN-only models'
    (roidb, dataset, start_ind, end_ind, total_num_images) = get_roidb_and_dataset(dataset_name, proposal_file, ind_range)
    model = initialize_model_from_cfg(weights_file, gpu_id=gpu_id)
    num_images = len(roidb)
    num_classes = cfg.MODEL.NUM_CLASSES
    (all_boxes, all_segms, all_keyps) = empty_results(num_classes, num_images)
    timers = defaultdict(Timer)
    for (i, entry) in enumerate(roidb):
        if cfg.TEST.PRECOMPUTED_PROPOSALS:
            box_proposals = entry['boxes'][(entry['gt_classes'] == 0)]
            if (len(box_proposals) == 0):
                continue
        else:
            box_proposals = None
        im = cv2.imread(entry['image'])
        with c2_utils.NamedCudaScope(gpu_id):
            (cls_boxes_i, cls_segms_i, cls_keyps_i) = im_detect_all(model, im, box_proposals, timers)
        extend_results(i, all_boxes, cls_boxes_i)
        if (cls_segms_i is not None):
            extend_results(i, all_segms, cls_segms_i)
        if (cls_keyps_i is not None):
            extend_results(i, all_keyps, cls_keyps_i)
        if ((i % 10) == 0):
            ave_total_time = np.sum([t.average_time for t in timers.values()])
            eta_seconds = (ave_total_time * ((num_images - i) - 1))
            eta = str(datetime.timedelta(seconds=int(eta_seconds)))
            det_time = ((timers['im_detect_bbox'].average_time + timers['im_detect_mask'].average_time) + timers['im_detect_keypoints'].average_time)
            misc_time = ((timers['misc_bbox'].average_time + timers['misc_mask'].average_time) + timers['misc_keypoints'].average_time)
            logger.info('im_detect: range [{:d}, {:d}] of {:d}: {:d}/{:d} {:.3f}s + {:.3f}s (eta: {})'.format((start_ind + 1), end_ind, total_num_images, ((start_ind + i) + 1), (start_ind + num_images), det_time, misc_time, eta))
        if cfg.VIS:
            im_name = os.path.splitext(os.path.basename(entry['image']))[0]
            vis_utils.vis_one_image(im[:, :, ::(- 1)], '{:d}_{:s}'.format(i, im_name), os.path.join(output_dir, 'vis'), cls_boxes_i, segms=cls_segms_i, keypoints=cls_keyps_i, thresh=cfg.VIS_TH, box_alpha=0.8, dataset=dataset, show_class=True)
    cfg_yaml = yaml.dump(cfg)
    if (ind_range is not None):
        det_name = ('detection_range_%s_%s.pkl' % tuple(ind_range))
    else:
        det_name = 'detections.pkl'
    det_file = os.path.join(output_dir, det_name)
    save_object(dict(all_boxes=all_boxes, all_segms=all_segms, all_keyps=all_keyps, cfg=cfg_yaml), det_file)
    logger.info('Wrote detections to: {}'.format(os.path.abspath(det_file)))
    return (all_boxes, all_segms, all_keyps)
