import os, sys
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import numpy as np
from modules.patchup import PatchUp, PatchUpMode
from modules.drop_block import DropBlock
from utility.utils import to_one_hot
from modules.mixup import mixup_process, get_lambda
from modules.cutmix import CutMix
from data_loader import per_image_standardization
import random


def get_layer_mix_lam(self, lam, lam_selection, max_rank_glb, k):
    lam_value = None
    if (type(lam) == type(None)):
        layer_mix = random.randint(1, k)
    else:
        if max_rank_glb:
            (data, layer_mix) = torch.max(lam[0][:k], 0)
        else:
            (data, layer_mix) = torch.min(lam[0][:k], 0)
        layer_mix = (layer_mix.item() + 1)
        if lam_selection:
            lam_value = data
            lam_value = torch.from_numpy(np.array([lam_value]).astype('float32')).to(device)
            lam_value = Variable(lam_value)
    return (lam_value, layer_mix)
