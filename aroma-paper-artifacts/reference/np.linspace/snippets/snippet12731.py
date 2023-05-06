import torch
import torch.nn as nn
import torch.nn.functional as F
from vocoder.distribution import sample_from_discretized_mix_logistic
from vocoder.display import *
from vocoder.audio import *


def xfade_and_unfold(self, y, target, overlap):
    ' Applies a crossfade and unfolds into a 1d array.\n\n        Args:\n            y (ndarry)    : Batched sequences of audio samples\n                            shape=(num_folds, target + 2 * overlap)\n                            dtype=np.float64\n            overlap (int) : Timesteps for both xfade and rnn warmup\n\n        Return:\n            (ndarry) : audio samples in a 1d array\n                       shape=(total_len)\n                       dtype=np.float64\n\n        Details:\n            y = [[seq1],\n                 [seq2],\n                 [seq3]]\n\n            Apply a gain envelope at both ends of the sequences\n\n            y = [[seq1_in, seq1_target, seq1_out],\n                 [seq2_in, seq2_target, seq2_out],\n                 [seq3_in, seq3_target, seq3_out]]\n\n            Stagger and add up the groups of samples:\n\n            [seq1_in, seq1_target, (seq1_out + seq2_in), seq2_target, ...]\n\n        '
    (num_folds, length) = y.shape
    target = (length - (2 * overlap))
    total_len = ((num_folds * (target + overlap)) + overlap)
    silence_len = (overlap // 2)
    fade_len = (overlap - silence_len)
    silence = np.zeros(silence_len, dtype=np.float64)
    t = np.linspace((- 1), 1, fade_len, dtype=np.float64)
    fade_in = np.sqrt((0.5 * (1 + t)))
    fade_out = np.sqrt((0.5 * (1 - t)))
    fade_in = np.concatenate([silence, fade_in])
    fade_out = np.concatenate([fade_out, silence])
    y[(:, :overlap)] *= fade_in
    y[(:, (- overlap):)] *= fade_out
    unfolded = np.zeros(total_len, dtype=np.float64)
    for i in range(num_folds):
        start = (i * (target + overlap))
        end = ((start + target) + (2 * overlap))
        unfolded[start:end] += y[i]
    return unfolded
