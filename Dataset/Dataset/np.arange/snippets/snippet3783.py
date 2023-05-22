import math
import numpy as np
import numpy.random as npr
import torch
import torch.utils.data as data
import torch.utils.data.sampler as torch_sampler
from torch.utils.data.dataloader import default_collate
from torch._six import int_classes as _int_classes
from core.config import cfg
from roi_data_rel.minibatch_rel import get_minibatch
import utils.blob as blob_utils


def __iter__(self):
    if cfg.TRAIN.ASPECT_GROUPING:
        (n, rem) = divmod(self.num_data, cfg.TRAIN.IMS_PER_BATCH)
        round_num_data = (n * cfg.TRAIN.IMS_PER_BATCH)
        indices = np.arange(round_num_data)
        npr.shuffle(indices.reshape((- 1), cfg.TRAIN.IMS_PER_BATCH))
        if (rem != 0):
            indices = np.append(indices, np.arange(round_num_data, (round_num_data + rem)))
        ratio_index = self.ratio_index[indices]
        ratio_list_minibatch = self.ratio_list_minibatch[indices]
    else:
        rand_perm = npr.permutation(self.num_data)
        ratio_list = self.ratio_list[rand_perm]
        ratio_index = self.ratio_index[rand_perm]
        ratio_list_minibatch = cal_minibatch_ratio(ratio_list)
    return iter(zip(ratio_index.tolist(), ratio_list_minibatch.tolist()))
