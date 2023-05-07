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


def forward(self, x, target=None, mixup=False, manifold_mixup=False, alpha=None, lam=None, patchup=False, dropblock=False, epoch=None, patchup_type=PatchUpMode.SOFT, k=2, dropblock_all=False):
    if self.per_img_std:
        x = per_image_standardization(x)
    lam_value = None
    if (manifold_mixup or patchup):
        layer_mix = random.randint(0, k)
    elif (dropblock and (not dropblock_all)):
        layer_mix = random.randint(1, k)
    elif mixup:
        layer_mix = 0
    else:
        layer_mix = None
    out = x
    if ((alpha is not None) and (type(lam_value) == type(None))):
        lam_value = get_lambda(alpha)
        lam_value = torch.from_numpy(np.array([lam_value]).astype('float32')).to(device)
        lam_value = Variable(lam_value)
    if (target is not None):
        target_reweighted = to_one_hot(target, self.num_classes)
    if ((layer_mix == 0) and patchup):
        cutmix = CutMix(beta=1.0)
        (target_a, target_b, out, portion) = cutmix.apply(inputs=out, target=target)
        target_a = to_one_hot(target_a, self.num_classes)
        target_b = to_one_hot(target_b, self.num_classes)
        target_reweighted = ((portion * target_a) + ((1.0 - portion) * target_b))
    elif ((layer_mix == 0) and (not patchup)):
        (out, target_reweighted) = mixup_process(out, target_reweighted, lam=lam_value)
    out = self.conv1(out)
    if ((not patchup) and (not dropblock) and ((layer_mix == 1) and (layer_mix <= k))):
        (out, target_reweighted) = mixup_process(out, target_reweighted, lam=lam_value)
    elif (patchup and ((layer_mix == 1) and (layer_mix <= k))):
        (target_a, target_b, target_reweighted, out, portion) = self.patchup_0(out, target_reweighted, lam=lam_value, patchup_type=patchup_type)
    if ((dropblock and dropblock_all and (1 <= k)) or (dropblock and (layer_mix == 1) and (layer_mix <= k))):
        out = self.dropblock(out)
    out = self.layer1(out)
    if ((not patchup) and (not dropblock) and (layer_mix == 2) and (layer_mix <= k)):
        (out, target_reweighted) = mixup_process(out, target_reweighted, lam=lam_value)
    elif (patchup and (layer_mix == 2) and (layer_mix <= k)):
        (target_a, target_b, target_reweighted, out, portion) = self.patchup_0(out, target_reweighted, lam=lam_value, patchup_type=patchup_type)
    if ((dropblock and dropblock_all and (2 <= k)) or (dropblock and (layer_mix == 2) and (layer_mix <= k))):
        out = self.dropblock(out)
    out = self.layer2(out)
    if ((not patchup) and (not dropblock) and (layer_mix == 3) and (layer_mix <= k)):
        (out, target_reweighted) = mixup_process(out, target_reweighted, lam=lam_value)
    elif (patchup and (layer_mix == 3) and (layer_mix <= k)):
        (target_a, target_b, target_reweighted, out, portion) = self.patchup_0(out, target_reweighted, lam=lam_value, patchup_type=patchup_type)
    if ((dropblock and dropblock_all and (3 <= k)) or (dropblock and (layer_mix == 3) and (layer_mix <= k))):
        out = self.dropblock(out)
    out = self.layer3(out)
    if ((not patchup) and (not dropblock) and (layer_mix == 4) and (layer_mix <= k)):
        (out, target_reweighted) = mixup_process(out, target_reweighted, lam=lam_value)
    elif (patchup and (layer_mix == 4) and (layer_mix <= k)):
        (target_a, target_b, target_reweighted, out, portion) = self.patchup_0(out, target_reweighted, lam=lam_value, patchup_type=patchup_type)
    if ((dropblock and dropblock_all and (4 <= k)) or (dropblock and (layer_mix == 4) and (layer_mix <= k))):
        out = self.dropblock(out)
    out = self.layer4(out)
    out = F.avg_pool2d(out, 4)
    out = out.view(out.size(0), (- 1))
    out = self.linear(out)
    if (target is not None):
        if patchup:
            return (target_a, target_b, target_reweighted, out, portion)
        return (out, target_reweighted)
    else:
        return out
