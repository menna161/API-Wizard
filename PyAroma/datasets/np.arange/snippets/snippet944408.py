import numpy as np
import torch
from fairseq.data.monolingual_dataset import MonolingualDataset
from . import FairseqDataset


def ordered_indices(self):
    return np.arange(len(self.dataset))
