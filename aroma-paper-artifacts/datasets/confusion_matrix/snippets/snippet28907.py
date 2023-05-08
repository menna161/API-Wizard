from nbdt.utils import set_np_printoptions, Colors
from nbdt.graph import wnid_to_synset, synset_to_wnid
from nbdt.model import SoftEmbeddedDecisionRules as SoftRules, HardEmbeddedDecisionRules as HardRules
from torch.distributions import Categorical
import torch.nn.functional as F
from collections import defaultdict
import torch
from nbdt import metrics
import functools
import numpy as np
import os
from PIL import Image
from pathlib import Path
import time


@staticmethod
def update(confusion_matrix, preds, labels):
    preds = tuple(preds)
    labels = tuple(labels)
    for (pred, label) in zip(preds, labels):
        confusion_matrix[(label, pred)] += 1
