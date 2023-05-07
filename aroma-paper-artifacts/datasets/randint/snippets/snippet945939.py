import os
import numpy as np
import sys
import torch
import torch.nn.functional as F
from .. import FairseqDataset
import soundfile as sf


def crop_to_max_size(self, wav, target_size):
    size = len(wav)
    diff = (size - target_size)
    if (diff <= 0):
        return wav
    start = np.random.randint(0, (diff + 1))
    end = ((size - diff) + start)
    return wav[start:end]
