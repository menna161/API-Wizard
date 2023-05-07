import numpy as np
import torch
import math
from . import data_utils, FairseqDataset


def permute_sentences(self, source, p=1.0):
    full_stops = (source == self.full_stop_index)
    full_stops[(- 2)] = 1
    sentence_ends = ((full_stops[1:] * (~ full_stops[:(- 1)])).nonzero() + 2)
    result = source.clone()
    num_sentences = sentence_ends.size(0)
    num_to_permute = math.ceil((((num_sentences * 2) * p) / 2.0))
    substitutions = torch.randperm(num_sentences)[:num_to_permute]
    ordering = torch.arange(0, num_sentences)
    ordering[substitutions] = substitutions[torch.randperm(num_to_permute)]
    index = 1
    for i in ordering:
        sentence = source[(sentence_ends[(i - 1)] if (i > 0) else 1):sentence_ends[i]]
        result[index:(index + sentence.size(0))] = sentence
        index += sentence.size(0)
    return result
