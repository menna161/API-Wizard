import torch.nn as nn
import torch
import torch.nn.functional as F
from ltr.models.layers.blocks import conv_block
import ltr.models.layers.filter as filter_layer
import math


def forward(self, train_feat, test_feat, train_bb, train_label, is_distractor=None, test_label=None, test_anno=None):
    'Order of dimensions should always be images_in_sequence before sequence.'
    train_feat = self.extract_classification_feat(train_feat)
    test_feat = self.extract_classification_feat(test_feat)
    if (self.jitter_sigma_factor is not None):
        train_bb_optim = train_bb.clone()
        train_bb_optim[(..., 0:2)] = (train_bb_optim[(..., 0:2)] + ((torch.randn_like(train_bb_optim[(..., 0:2)]) * train_bb_optim[(..., 2:)].prod(dim=(- 1), keepdim=True).sqrt()) * self.jitter_sigma_factor))
    else:
        train_bb_optim = train_bb
    (filter, losses) = self.get_filter(train_feat, train_bb, train_label, is_distractor=is_distractor, train_bb=train_bb_optim, test_feat=test_feat, test_label=test_label, test_anno=test_anno)
    test_scores = self.classify(filter, test_feat)
    return (test_scores, losses)
