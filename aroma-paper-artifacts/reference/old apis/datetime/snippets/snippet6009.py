from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import cv2
import datetime
import logging
import numpy as np
import os
import yaml
from caffe2.python import core
from caffe2.python import workspace
from detectron.core.config import cfg
from detectron.datasets import task_evaluation
from detectron.datasets.json_dataset import JsonDataset
from detectron.modeling import model_builder
from detectron.utils.io import save_object
from detectron.utils.timer import Timer
import detectron.utils.blob as blob_utils
import detectron.utils.c2 as c2_utils
import detectron.utils.env as envu
import detectron.utils.net as nu
import detectron.utils.subprocess as subprocess_utils


def generate_proposals_on_roidb(model, roidb, start_ind=None, end_ind=None, total_num_images=None, gpu_id=0):
    'Generate RPN proposals on all images in an imdb.'
    _t = Timer()
    num_images = len(roidb)
    roidb_boxes = [[] for _ in range(num_images)]
    roidb_scores = [[] for _ in range(num_images)]
    roidb_ids = [[] for _ in range(num_images)]
    if (start_ind is None):
        start_ind = 0
        end_ind = num_images
        total_num_images = num_images
    for i in range(num_images):
        roidb_ids[i] = roidb[i]['id']
        im = cv2.imread(roidb[i]['image'])
        with c2_utils.NamedCudaScope(gpu_id):
            _t.tic()
            (roidb_boxes[i], roidb_scores[i]) = im_proposals(model, im)
            _t.toc()
        if ((i % 10) == 0):
            ave_time = _t.average_time
            eta_seconds = (ave_time * ((num_images - i) - 1))
            eta = str(datetime.timedelta(seconds=int(eta_seconds)))
            logger.info('rpn_generate: range [{:d}, {:d}] of {:d}: {:d}/{:d} {:.3f}s (eta: {})'.format((start_ind + 1), end_ind, total_num_images, ((start_ind + i) + 1), (start_ind + num_images), ave_time, eta))
    return (roidb_boxes, roidb_scores, roidb_ids)
