from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
import six
import logging
import numpy as np
import utils.boxes as box_utils
import utils.blob as blob_utils
from core.config import cfg
from .json_dataset_rel import JsonDatasetRel


def _compute_and_log_stats(roidb):
    classes = roidb[0]['dataset'].classes
    char_len = np.max([len(c) for c in classes])
    hist_bins = np.arange((len(classes) + 1))
    gt_hist = np.zeros(len(classes), dtype=np.int)
    for entry in roidb:
        gt_inds = np.where(((entry['gt_classes'] > 0) & (entry['is_crowd'] == 0)))[0]
        gt_classes = entry['gt_classes'][gt_inds]
        gt_hist += np.histogram(gt_classes, bins=hist_bins)[0]
    logger.debug('Ground-truth class histogram:')
    for (i, v) in enumerate(gt_hist):
        logger.debug('{:d}{:s}: {:d}'.format(i, classes[i].rjust(char_len), v))
    logger.debug(('-' * char_len))
    logger.debug('{:s}: {:d}'.format('total'.rjust(char_len), np.sum(gt_hist)))
