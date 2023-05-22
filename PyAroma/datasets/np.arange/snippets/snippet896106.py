import torch
import numpy as np
from fairseq.data import data_utils


def noising(self, x, lengths, max_shuffle_distance=None):
    if (max_shuffle_distance is None):
        max_shuffle_distance = self.default_max_shuffle_distance
    if (max_shuffle_distance == 0):
        return (x, lengths)
    assert (max_shuffle_distance > 1)
    noise = np.random.uniform(0, max_shuffle_distance, size=(x.size(0), x.size(1)))
    noise[0] = (- 1)
    word_idx = self.get_word_idx(x)
    x2 = x.clone()
    for i in range(lengths.size(0)):
        length_no_eos = lengths[i]
        if (x[((lengths[i] - 1), i)] == self.dictionary.eos()):
            length_no_eos = (lengths[i] - 1)
        scores = (word_idx[(:length_no_eos, i)] + noise[(word_idx[(:length_no_eos, i)], i)])
        scores += (1e-06 * np.arange(length_no_eos))
        permutation = scores.argsort()
        x2[(:length_no_eos, i)].copy_(x2[(:length_no_eos, i)][torch.from_numpy(permutation)])
    return (x2, lengths)
