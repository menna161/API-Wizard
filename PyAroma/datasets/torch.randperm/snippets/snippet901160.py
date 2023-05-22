from __future__ import division
import math
import random
import numpy as np
import torch
from torch import cuda
import onqg.dataset.Constants as Constants


def shuffle(self):
    'shuffle the order of data in every batch'

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
    assert (self.tgt != None), 'shuffle is only aimed for training data (with target given)'
    NEW = {'SRCs': [], 'TGTs': [], 'IDXs': []}
    if self.copy:
        (NEW['COPYSWTs'], NEW['COPYTGTs']) = ([], [])
    if self.feature_num:
        NEW['FTs'] = [[] for i in range(self.feature_num)]
    if self.answer:
        NEW['ANSs'] = []
        if self.ans_feature_num:
            NEW['ANSFTs'] = [[] for i in range(self.ans_feature_num)]
    shuffle_all = random.random()
    if (shuffle_all > 0.75):
        (start, end) = (0, (self.batchSize * self.numBatches))
        NEW = shuffle_group(start, end, NEW)
    else:
        for batch_idx in range(self.numBatches):
            start = (batch_idx * self.batchSize)
            end = (start + self.batchSize)
            NEW = shuffle_group(start, end, NEW)
    (self.src, self.tgt, self.idxs) = (NEW['SRCs'], NEW['TGTs'], NEW['IDXs'])
    if self.copy:
        (self.copy_switch, self.copy_tgt) = (NEW['COPYSWTs'], NEW['COPYTGTs'])
    if self.answer:
        self.ans = NEW['ANSs']
        if self.ans_feature_num:
            self.ans_features = NEW['ANSFTs']
    if self.feature_num:
        self.features = NEW['FTs']
