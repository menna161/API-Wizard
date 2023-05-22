import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
from math import pi, sqrt


def get_ohem_label(self, pred, label):
    (n, c, h, w) = pred.size()
    if (self.ignore_index is None):
        self.ignore_index = (c + 1)
    input_label = label.data.cpu().numpy().ravel().astype(np.int32)
    x = np.rollaxis(pred.data.cpu().numpy(), 1).reshape((c, (- 1)))
    input_prob = np.exp((x - x.max(axis=0, keepdims=True)))
    input_prob /= input_prob.sum(axis=0, keepdims=True)
    valid_flag = (input_label != self.ignore_index)
    valid_inds = np.where(valid_flag)[0]
    valid_label = input_label[valid_flag]
    num_valid = valid_flag.sum()
    if (self.min_kept >= num_valid):
        print('Labels: {}'.format(num_valid))
    elif (num_valid > 0):
        valid_prob = input_prob[(:, valid_flag)]
        valid_prob = valid_prob[(valid_label, np.arange(len(valid_label), dtype=np.int32))]
        threshold = self.thresh
        if (self.min_kept > 0):
            index = valid_prob.argsort()
            threshold_index = index[(min(len(index), self.min_kept) - 1)]
            if (valid_prob[threshold_index] > self.thresh):
                threshold = valid_prob[threshold_index]
        kept_flag = (valid_prob <= threshold)
        valid_kept_inds = valid_inds[kept_flag]
        valid_inds = valid_kept_inds
    self.ohem_ratio = (len(valid_inds) / num_valid)
    valid_kept_label = input_label[valid_inds].copy()
    input_label.fill(self.ignore_index)
    input_label[valid_inds] = valid_kept_label
    label = torch.from_numpy(input_label.reshape(label.size())).long().cuda()
    return label
