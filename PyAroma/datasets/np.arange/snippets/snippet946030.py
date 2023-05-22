import math
import numpy as np
import torch
from typing import Dict, List, Tuple
from fairseq.data import FairseqDataset, data_utils
from fairseq.data import Dictionary
from fairseq.data.legacy.block_pair_dataset import BlockPairDataset
from fairseq.data.token_block_dataset import TokenBlockDataset
from fairseq.data.concat_dataset import ConcatDataset


def ordered_indices(self):
    '\n        Return an ordered list of indices. Batches will be constructed based\n        on this order.\n        '
    if self.shuffle:
        return np.random.permutation(len(self))
    else:
        order = [np.arange(len(self))]
        order.append(self.sizes)
        return np.lexsort(order)
