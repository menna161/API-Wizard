import numpy as np
import torch
import math
from . import data_utils, FairseqDataset


def add_whole_word_mask(self, source, p):
    is_word_start = self.word_starts(source)
    num_to_mask = int(math.ceil((is_word_start.float().sum() * p)))
    num_inserts = 0
    if (num_to_mask == 0):
        return source
    if (self.mask_span_distribution is not None):
        lengths = self.mask_span_distribution.sample(sample_shape=(num_to_mask,))
        cum_length = torch.cumsum(lengths, 0)
        while (cum_length[(- 1)] < num_to_mask):
            lengths = torch.cat([lengths, self.mask_span_distribution.sample(sample_shape=(num_to_mask,))], dim=0)
            cum_length = torch.cumsum(lengths, 0)
        i = 0
        while (cum_length[i] < num_to_mask):
            i += 1
        lengths[i] = (num_to_mask - (0 if (i == 0) else cum_length[(i - 1)]))
        num_to_mask = (i + 1)
        lengths = lengths[:num_to_mask]
        lengths = lengths[(lengths > 0)]
        num_inserts = (num_to_mask - lengths.size(0))
        num_to_mask -= num_inserts
        if (num_to_mask == 0):
            return self.add_insertion_noise(source, (num_inserts / source.size(0)))
        assert (lengths > 0).all()
    else:
        lengths = torch.ones((num_to_mask,)).long()
    assert (is_word_start[(- 1)] == 0)
    word_starts = is_word_start.nonzero()
    indices = word_starts[torch.randperm(word_starts.size(0))[:num_to_mask]].squeeze(1)
    mask_random = (torch.FloatTensor(num_to_mask).uniform_() < self.random_ratio)
    source_length = source.size(0)
    assert ((source_length - 1) not in indices)
    to_keep = torch.ones(source_length, dtype=torch.bool)
    is_word_start[(- 1)] = 255
    if (self.replace_length == 0):
        to_keep[indices] = 0
    else:
        source[indices] = self.mask_idx
        source[indices[mask_random]] = torch.randint(1, len(self.vocab), size=(mask_random.sum(),))
    if (self.mask_span_distribution is not None):
        assert (len(lengths.size()) == 1)
        assert (lengths.size() == indices.size())
        lengths -= 1
        while (indices.size(0) > 0):
            assert (lengths.size() == indices.size())
            lengths -= is_word_start[(indices + 1)].long()
            uncompleted = (lengths >= 0)
            indices = (indices[uncompleted] + 1)
            mask_random = mask_random[uncompleted]
            lengths = lengths[uncompleted]
            if (self.replace_length != (- 1)):
                to_keep[indices] = 0
            else:
                source[indices] = self.mask_idx
                source[indices[mask_random]] = torch.randint(1, len(self.vocab), size=(mask_random.sum(),))
    else:
        while (indices.size(0) > 0):
            uncompleted = (is_word_start[(indices + 1)] == 0)
            indices = (indices[uncompleted] + 1)
            mask_random = mask_random[uncompleted]
            if (self.replace_length != (- 1)):
                to_keep[indices] = 0
            else:
                source[indices] = self.mask_idx
                source[indices[mask_random]] = torch.randint(1, len(self.vocab), size=(mask_random.sum(),))
            assert ((source_length - 1) not in indices)
    source = source[to_keep]
    if (num_inserts > 0):
        source = self.add_insertion_noise(source, (num_inserts / source.size(0)))
    return source
