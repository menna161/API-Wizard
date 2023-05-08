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
def normalize(confusion_matrix, axis):
    total = confusion_matrix.astype(np.float).sum(axis=axis)
    total = (total[(:, None)] if (axis == 1) else total[None])
    return (confusion_matrix / total)
