import torch
from torch.nn.init import xavier_normal_
import torch.nn as nn
import torch.nn.functional as F
from bert_feature_extractor import BertLayer
from decoder import DistMult, ConvE, ConvTransE, ConvKB
import layers


def mask_by_schedule(self, tensor, epoch, epoch_cutoff=100):
    if (epoch < epoch_cutoff):
        cuda_check = tensor.is_cuda
        if cuda_check:
            mask = torch.zeros((tensor.size(0), tensor.size(1)), device='cuda')
        else:
            mask = torch.zeros((tensor.size(0), tensor.size(1)))
        k = int(((epoch / epoch_cutoff) * tensor.size(1)))
        perm = torch.randperm(tensor.size(1))
        indices = perm[:k]
        mask[(:, indices)] = 1
        return (tensor * mask)
    else:
        return tensor
