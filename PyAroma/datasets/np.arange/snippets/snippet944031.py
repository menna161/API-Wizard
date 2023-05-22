import logging
import numpy as np
import torch
from fairseq.data import Dictionary, FairseqDataset
from fairseq.tasks import FairseqTask, register_task


def ordered_indices(self):
    return np.arange(self.num_items)
