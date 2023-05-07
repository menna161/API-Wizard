from __future__ import division
import math
import random
import numpy as np
import torch
from torch import cuda
import onqg.dataset.Constants as Constants


def shuffle_group(start, end, NEW):
    'shuffle the order of samples with index from start to end'
    RAW = [self.src[start:end], self.tgt[start:end], self.idxs[start:end]]
    DATA = list(zip(*RAW))
    index = torch.randperm(len(DATA))
    (src, tgt, idx) = zip(*[DATA[i] for i in index])
    NEW['SRCs'] += list(src)
    NEW['TGTs'] += list(tgt)
    NEW['IDXs'] += list(idx)
    if self.answer:
        ans = [self.ans[start:end][i] for i in index]
        NEW['ANSs'] += ans
        if self.ans_feature_num:
            ansft = [[feature[start:end][i] for i in index] for feature in self.ans_features]
            for i in range(self.ans_feature_num):
                NEW['ANSFTs'][i] += ansft[i]
    if self.feature_num:
        ft = [[feature[start:end][i] for i in index] for feature in self.features]
        for i in range(self.feature_num):
            NEW['FTs'][i] += ft[i]
    if self.copy:
        cpswt = [self.copy_switch[start:end][i] for i in index]
        cptgt = [self.copy_tgt[start:end][i] for i in index]
        NEW['COPYSWTs'] += cpswt
        NEW['COPYTGTs'] += cptgt
    return NEW
