import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data
from torchvision import transforms, utils
import numpy as np
import importlib
import random
import math
from sacred import Experiment
import util_func as util_func
import util_loss as util_loss
import util_data as util_data


def process_batch_data(self, input_batch, flag_same=False):
    (im_faces, im_lndm, im_msk, im_ind) = input_batch
    im_faces = [item.float().to(self.device_comp) for item in im_faces]
    im_lndm = [item.float().to(self.device_comp) for item in im_lndm]
    im_msk = [item.float().to(self.device_comp) for item in im_msk]
    labels_one_hot = np.zeros((int(im_faces[0].shape[0]), self.num_classes))
    if (len(im_ind) > 1):
        labels_one_hot[(np.arange(int(im_faces[1].shape[0])), im_ind[1])] = 1
    labels_one_hot = torch.tensor(labels_one_hot).float().to(self.device_comp)
    if flag_same:
        if (len(im_ind) > 1):
            label_same = ((im_ind[0] == im_ind[1]) / 1)
        else:
            label_same = ((im_ind[0] == im_ind[0]) / 1)
        return (im_faces, im_lndm, im_msk, labels_one_hot, label_same.to(self.device_comp))
    return (im_faces, im_lndm, im_msk, labels_one_hot)
