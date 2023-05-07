import os
import numpy as np
import sys
import torch
import torch.nn.functional as F
from .. import FairseqDataset
import soundfile as sf


def collater(self, samples):
    samples = [s for s in samples if ((s['source'] is not None) and (len(s['source']) > 0))]
    if (len(samples) == 0):
        return {}
    sources = [s['source'] for s in samples]
    sizes = [len(s) for s in sources]
    target_size = min(min(sizes), self.max_sample_size)
    if (target_size < self.min_length):
        return {}
    if (self.min_sample_size < target_size):
        target_size = np.random.randint(self.min_sample_size, (target_size + 1))
    collated_sources = sources[0].new(len(sources), target_size)
    for (i, (source, size)) in enumerate(zip(sources, sizes)):
        diff = (size - target_size)
        assert (diff >= 0)
        if (diff == 0):
            collated_sources[i] = source
        else:
            collated_sources[i] = self.crop_to_max_size(source, target_size)
    return {'id': torch.LongTensor([s['id'] for s in samples]), 'net_input': {'source': collated_sources}}
