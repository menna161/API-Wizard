import math
import numpy as np
import torch
from fairseq.data import FairseqDataset


def _skip_sampling(self, total, skip_ids):
    '\n        Generate a random integer which is not in skip_ids. Sample range is [0, total)\n        TODO: ids in skip_ids should be consecutive, we can extend it to more generic version later\n        '
    rand_id = np.random.randint((total - len(skip_ids)))
    return (rand_id if (rand_id < min(skip_ids)) else (rand_id + len(skip_ids)))
