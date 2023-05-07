import os
import numpy as np
from fairseq.data import FairseqDataset
from . import data_utils
from .collaters import Seq2SeqCollater
import torchaudio
import torchaudio.compliance.kaldi as kaldi


def ordered_indices(self):
    'Return an ordered list of indices. Batches will be constructed based\n        on this order.'
    return np.arange(len(self))
